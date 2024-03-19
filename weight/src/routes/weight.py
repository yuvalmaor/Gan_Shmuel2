from flask import request, jsonify, Blueprint
from datetime import datetime
from ..models import Transaction, Container
from ..config import logger
import random
from ..utils.weight import calc_containers_weights, calc_transaction_neto
from ..database import db

weight_blueprint = Blueprint('weight_blueprint', __name__)


@weight_blueprint.route('/weight', methods=['GET'])
def get_weights():
    logger.info("Received request to retrieve transactions")

    from_date_str = request.args.get('from')
    to_date_str = request.args.get('to')
    filter_directions = request.args.get('filter', 'in,out,none').replace('"', '').split(',')
    valid_filters = ['in','out','none']

    invalid_filters = [f for f in filter_directions if f not in valid_filters]
    if invalid_filters:
        return jsonify({"error": f"Invalid filter value(s): {', '.join(invalid_filters)}. Allowed values are: in, out, none"}), 400
    
    try:
        if from_date_str:
            from_date = datetime.strptime(from_date_str, '%Y%m%d%H%M%S')
        else:
            from_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        if to_date_str:
            to_date = datetime.strptime(to_date_str, '%Y%m%d%H%M%S')
        else:
            to_date = datetime.now()

    except ValueError:
        return jsonify({"error": "The provided date parameters are not valid. Ensure they are in the 'YYYYMMDDHHMMSS' format."}), 400
    
    # database queries
    logger.info(
        f"Retrieving transactions from {from_date} to {to_date} with filter directions: {filter_directions}")

    try:
        transactions = Transaction.query.filter(
            Transaction.datetime >= from_date,
            Transaction.datetime <= to_date,
            Transaction.direction.in_(filter_directions)
        ).all()
    except:
        return jsonify({"error": "Can't get transactions from the database"}), 500

    logger.info(
        f"Retrieved {len(transactions)} transactions from the database")

    response = [{
        "ID": transaction.id,
        "direction": transaction.direction,
        "bruto": transaction.bruto,
        "neto": transaction.neto if transaction.neto is not None else "na",
        "produce": transaction.produce,
        "containers": transaction.containers.split(',') if transaction.containers else [],
        "session_id": transaction.session_id
    } for transaction in transactions]

    logger.info(f"Returning {len(response)} transactions in the response")

    return jsonify(response), 200

#!create better verifications for the request body
@weight_blueprint.route('/weight', methods=['POST'])
def create_weight():


    def weight_container(container_id:str, unit:str, weight:int):
        container = Container.query.filter(Container.container_id == container_id).first()
        if not container:
            container = Container(container_id=container_id, weight=weight, unit=unit)
        container.weight = weight
        container.unit = unit
        return container

    def build_response(transaction: Transaction, direction: str):
        res = dict()
        
        res["id"] = transaction.id
        res["bruto"] = transaction.bruto
        res["truck"] = transaction.truck
        if direction == "out":
            res["truckTara"] = transaction.truckTara
            res["neto"] = transaction.neto or "na"
        return res
    
    def force_edit(last_transaction:Transaction, direction:str, weight:int, truck:str, containers:list[str], date:datetime = datetime.now()):
        last_transaction.truck = truck
        last_transaction.datetime = date
        if direction == "in":
            last_transaction.bruto = weight
            last_transaction.containers = containers
        else:
            if last_transaction.neto != None:
                last_transaction.neto = last_transaction.neto + last_transaction.truckTara - weight
            last_transaction.truckTara = weight
        return last_transaction

    logger.info("Received request to create a weight transaction")
    print(request)
    data = request.get_json()
    #! direction: no actual default
    #! truck: if none in direction then 'na' (do we need to actually use 'na' outside of the response?)
    #! containers: can be an empty string
    #! weight is dependent on the direction
    #! produce : default 'na' (do we even need the 'na'?)
    direction = data.get("direction")
    truck = data.get("truck")
    containers = data.get("containers") or ""
    weight = data.get("weight")
    unit = data.get("unit")
    force = data.get("force") or False
    produce = data.get("produce") or "na"

    
    if not direction or not weight or not unit or not truck:
        return {"error": "Invalid request, the direction, weight, unit, truck are required"}, 401
    
    if truck == "na" and not containers:
        return {"error": "Invalid request, need to specify containers when not specifing truck"}, 401

    curr_date = datetime.now()

    last_transaction = Transaction.query.order_by(Transaction.id.desc()).first()
    if last_transaction:
        if last_transaction.direction == "in" and direction == "none":
                return {"error": "Cant do none direction after in"}, 400
        if direction != "none":
            if last_transaction.direction == direction:
                if not force:
                    return {"error": f"Cant do {last_transaction.direction} direction after {direction}"}, 400
                if force:
                    last_transaction = force_edit(last_transaction, direction, weight, truck, containers, curr_date)
                    db.session.add(last_transaction)
                    db.session.commit()
                    return build_response(last_transaction,direction), 200
    
    session_id  = random.randint(0, 2_000_000)

    if direction == "none":
        if produce == "na":
            container = weight_container(containers, unit, weight)
            db.session.add(container)
        transaction = Transaction(direction=direction,truck=truck,datetime=curr_date ,containers=containers, produce=produce,
                                  bruto=weight, session_id=session_id)
        db.session.add(transaction)
        db.session.commit()
        db.session.refresh(transaction)
        return build_response(transaction, direction), 200

    if direction == "in":
        transaction = Transaction(direction=direction,truck=truck, datetime=curr_date, containers=containers, bruto=weight, 
                                  session_id=session_id, produce=produce)
        # calc containers
        db.session.add(transaction)
        db.session.commit()
        db.session.refresh(transaction)
        return build_response(transaction, direction), 200

    if direction == "out":
        last_transaction : Transaction = Transaction.query.order_by(Transaction.id.desc()).filter(Transaction.truck == truck, Transaction.direction == "in").first()
        
        if(not last_transaction):
            return {"error": "Cant do out without an in"}, 400
        
        containers_id = last_transaction.containers.split(",")
        db_containers : list[Container] = Container.query.filter(Container.container_id.in_(containers_id)).all()
        neto_price = None
        if len(containers_id) == len(db_containers):
            containers_weight = calc_containers_weights([(container.weight, container.unit) for container in db_containers], unit)
            neto_price = containers_weight and calc_transaction_neto(last_transaction.bruto, weight, containers_weight)
        else:
            unregistered_containers =  set(containers_id)-set([container.container_id for container in db_containers])
            logger.info(f"Inserting containers with ids- {unregistered_containers}")
            db.session.add_all([Container(container_id=container_id, unit=unit, weight=None) for container_id in unregistered_containers])
    
        new_transaction = Transaction(truck=truck,datetime=curr_date ,bruto=last_transaction.bruto,
                                       truckTara=weight, direction="out", neto=neto_price, produce=last_transaction.produce, session_id=last_transaction.session_id)
        db.session.add(new_transaction)
        db.session.commit()
        db.session.refresh(new_transaction)
        return build_response(new_transaction, direction), 200

        

        

