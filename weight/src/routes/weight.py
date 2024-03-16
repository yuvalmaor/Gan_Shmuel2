from flask import request, jsonify, Blueprint
from datetime import datetime
from ..models import Transaction, Container
from ..config import logger
import string
import secrets
from ..utils.weight import calc_containers_weights, calc_transaction_neto
from ..database import db

weight_blueprint = Blueprint('weight_blueprint', __name__)


@weight_blueprint.route('/weight', methods=['GET'])
def get_weights():
    logger.info("Received request to retrieve transactions")

    from_date_str = request.args.get(
        'from', datetime.now().strftime('%Y%m%d') + '000000')
    to_date_str = request.args.get(
        'to', datetime.now().strftime('%Y%m%d%H%M%S'))
    filter_directions = request.args.get(
        'filter', 'in,out,none').replace('"', '').split(',')

    from_date = datetime.strptime(from_date_str, '%Y%m%d%H%M%S')
    to_date = datetime.strptime(to_date_str, '%Y%m%d%H%M%S')

    # database queries
    logger.info(
        f"Retrieving transactions from {from_date} to {to_date} with filter directions: {filter_directions}")

    #! add a try and except
    transactions = Transaction.query.filter(
        Transaction.datetime >= from_date,
        Transaction.datetime <= to_date,
        Transaction.direction.in_(filter_directions)
    ).all()

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


@weight_blueprint.route('/weight', methods=['POST'])
def create_weight():
    data = dict(request.json)
    #! direction: no actual default
    #! truck: if none in direction then 'na'
    #! containers: can be an empty string
    #! weight is dependent on the direction
    #! produce : default 'na'
    direction = data.get("direction")
    truck = data.get("truck", "na")
    containers = data.get("containers","")
    weight = data.get("weight")
    unit = data.get("unit")
    force = data.get("force", False)
    produce = data.get("produce", "na")

    if not direction or not weight or not unit:
        return jsonify({"error":"Invalid request, the params direction, weight, unit are required"}), 400
    if direction not in {"in", "out", "none"}:
        return jsonify({"error":"Invalid request, Invalid direction"}), 400
 
    #if direction none and has a truck number return an error
    transactions : list[Transaction] = []
    if(direction == 'none'):
        if(truck is not 'na'):
            return jsonify({"error":"Cannot have a truck licence associated with a container."}), 400
        transactions = Transaction.query.all()
    else:
        transactions = Transaction.query.order_by(Transaction.datetime).filter(Transaction.truck == truck).all()      

    former_transaction = transactions[-1] if transactions else None
    if not former_transaction:
        if direction == "out":
            return jsonify({"error": "Cannot create an 'out' transaction without an existing 'in' transaction."}), 400 
    else:
        # none after in returns an error
        if (former_transaction.direction == 'in' and direction == 'none'):
            return jsonify({"error": "Cannot create a 'none' transaction after an 'in' transaction."}), 400
        # update weight if in after in or out after out
        if ((direction == 'in' and former_transaction.direction == 'in') or (direction == 'out' and former_transaction.direction == 'out')):
            if (force):
                try:
                    if (direction == 'in'):
                        former_transaction.bruto = weight
                        db.session.commit()
                        return {
                            "id": former_transaction.id,
                            "truck": former_transaction.truck,
                            "bruto": former_transaction.bruto
                        }
                    else:
                        #! need to check about the calculation of the containers
                        former_transaction.truckTara = weight                        
                        db.session.commit()
                        return {
                            "id": former_transaction.id,
                            "truck": former_transaction.truck,
                            "bruto": former_transaction.bruto,
                            "truckTara": former_transaction.truckTara,
                            "neto": former_transaction.neto
                        }, 200
                except:
                    return jsonify({"error": "Couldn't update weight"}), 500
            else:
                return jsonify({"error": "Invalid transaction sequence"}), 500

    #----------------------------------------------------
            
    date_time_now = datetime.now()
    new_transaction = None
    if direction == "in" or direction == "none":           
        alphabet = string.digits
        session_id = ''.join(secrets.choice(alphabet) for _ in range(12))
        new_transaction = Transaction(datetime=date_time_now, bruto=int(weight), direction=direction,
                                        truck=truck, containers=containers, produce=produce,
                                        session_id=session_id)

    if direction == "out":

        used_containers_weights = Container.query.with_entities(Container.weight, Container.unit).filter(
            Container.container_id.in_(former_transaction.containers.split(","))).all()
        num_of_containers = len(former_transaction.containers.split(","))
        containers_weight = calc_containers_weights(
            used_containers_weights, unit) if num_of_containers == len(used_containers_weights) else None

        print(used_containers_weights)
        print(containers_weight)
        neto = calc_transaction_neto(
            former_transaction.bruto, weight, containers_weight) if containers_weight else None
        
        new_transaction = Transaction(truck=truck, direction = direction, datetime=date_time_now, 
                                    containers=containers, bruto = former_transaction.bruto, neto=neto,
                                    truckTara=weight, produce=produce, session_id=former_transaction.session_id)
    
    
    try:
        db.session.add(new_transaction)
        db.session.commit()
        db.session.refresh(new_transaction)
    
    except Exception as e:
        return jsonify({"error": "Cannot add transaction"}), 500

    res = {
        "id": new_transaction.id,
        "truck": new_transaction.truck,
        "bruto": new_transaction.bruto
    }
    if direction == "out":
        res["truckTara"] = new_transaction.truckTara
        res["neto"] = new_transaction.neto or "na"
    return res, 200
