from flask import request, jsonify, Blueprint
from datetime import datetime
from ..models import Transaction, Container
from ..config import logger
import string,secrets
from ..utils.weight import caclc_containers_weights, calc_transaction_neto
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
    alphabet = string.digits
    data = request.json
    date = datetime.now()
    direction, truck, containers, weight ,unit, force, produce = data.get("direction","none"), data.get("truck","na"), data.get("containers"), data.get("weight") ,data.get("unit"), data.get("force"), data.get("produce","na")
    if direction == "in":
        session_id = ''.join(secrets.choice(alphabet) for _ in range(12))
        new_transaction = Transaction(datetime=date, bruto=int(weight) ,direction=direction, 
                                      truck=truck,containers=containers, produce=produce,
                                      session_id=session_id)
        with db.session() as session:
            session.add(new_transaction)
            session.commit()
            session.refresh(new_transaction)
        
        return {
            "id": new_transaction.id,
            "truck" : new_transaction.truck,
            "bruto" : new_transaction.bruto
        }
    if direction == "out":
        transactions = Transaction.query.filter(Transaction.truck == truck).all()
        if not transactions:
            return "Error", 500
        curr_transaction : Transaction = transactions[-1]
        if curr_transaction.direction == "out":
            return "Error", 500
        
        curr_transaction.truckTara = weight
        used_containers_weights = Container.query.with_entities(Container.weight, Container.unit).filter(Container.container_id.in_(curr_transaction.containers.split(","))).all()
        containers_weight = caclc_containers_weights(used_containers_weights, unit)
        curr_transaction.neto = calc_transaction_neto(curr_transaction.bruto, curr_transaction.truckTara, containers_weight)


        curr_transaction.direction = "out"
        return {
            "id" : curr_transaction.id,
            "truck" : curr_transaction.truck,
            "bruto" : curr_transaction.bruto,
            "truckTara" : curr_transaction.truckTara,
            "neto" : curr_transaction.neto
        }, 200
