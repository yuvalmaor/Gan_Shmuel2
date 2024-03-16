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

#!create better verifications for the request body
@weight_blueprint.route('/weight', methods=['POST'])
def create_weight():
    logger.info("Received request to create a weight transaction")

    data = dict(request.json)
    #! direction: no actual default
    #! truck: if none in direction then 'na' (do we need to actually use 'na' outside of the response?)
    #! containers: can be an empty string
    #! weight is dependent on the direction
    #! produce : default 'na' (do we even need the 'na'?)
    direction = data.get("direction")
    truck = data.get("truck", "na") # do i need to use the 'na' outside of the response?
    containers = data.get("containers", "")
    weight = data.get("weight")
    unit = data.get("unit")
    force = data.get("force", False)
    produce = data.get("produce", "na") # do i need to use the 'na' outside of the response?

    if not direction or not weight or not unit:
        logger.error(
            "Invalid request: Missing required parameters direction, weight, or unit")
        return jsonify({"error": "Invalid request, the params direction, weight, unit are required"}), 400
    if direction not in {"in", "out", "none"}:
        logger.error("Invalid direction provided in the request")
        return jsonify({"error": "Invalid request, Invalid direction"}), 400

    # if direction none and has a truck number return an error
    #query all or only a specific truck
    transactions: list[Transaction] = []
    if (direction == 'none'):
        if (truck != 'na'):
            logger.error(
                "Truck license provided for a 'none' direction transaction")
            return jsonify({"error": "Cannot have a truck licence associated with a container."}), 400
        transactions = Transaction.query.all()
    else:
        transactions = Transaction.query.order_by(
            Transaction.datetime).filter(Transaction.truck == truck).all()

    logger.info(
        "Processing transactions based on direction and truck information")

    former_transaction = transactions[-1] if transactions else None
    if not former_transaction:
        if direction == "out":
            logger.error(
                "Attempting to create an 'out' transaction without an 'in' transaction")
            return jsonify({"error": "Cannot create an 'out' transaction without an existing 'in' transaction."}), 400
    else:
        # none after in returns an error
        if (former_transaction.direction == 'in' and direction == 'none'):
            logger.error("Invalid transaction sequence: 'none' after 'in'")
            return jsonify({"error": "Cannot create a 'none' transaction after an 'in' transaction."}), 400
        # update weight if in after in or out after out
        if ((direction == 'in' and former_transaction.direction == 'in') or (direction == 'out' and former_transaction.direction == 'out')):
            if (force):
                try:
                    transaction_response = {
                        "id": former_transaction.id,
                        "truck": former_transaction.truck,
                        "bruto": former_transaction.bruto
                    }
                    if (direction == 'in'):
                        former_transaction.bruto = weight
                        db.session.commit()
                    else:
                        #! need to check about the calculation of the containers
                        former_transaction.truckTara = weight
                        transaction_response["truckTara"] = former_transaction.truckTara
                        transaction_response["neto"] = former_transaction.neto
                    db.session.commit()
                    logger.info(
                        f"Transaction with ID {former_transaction.id} updated successfully")
                    return transaction_response, 200
                except Exception as e:
                    logger.error(f"Failed to update transaction: {str(e)}")
                    return jsonify({"error": "Failed to update transaction"}), 500
            else:
                logger.error("Invalid transaction sequence without force flag")
                # conflict with the rules of the app but not really with the entities so not 409
                return jsonify({"error": "Invalid transaction sequence"}), 422

    # New transaction creation logic here
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

        new_transaction = Transaction(truck=truck, direction=direction, datetime=date_time_now,
                                      containers=containers, bruto=former_transaction.bruto, neto=neto,
                                      truckTara=weight, produce=produce, session_id=former_transaction.session_id)

    try:
        db.session.add(new_transaction)
        db.session.commit()
        db.session.refresh(new_transaction)
        logger.info(
            f"New transaction with ID {new_transaction.id} created successfully")
    except Exception as e:
        logger.error(f"Failed to add new transaction: {str(e)}")
        return jsonify({"error": "Cannot add transaction"}), 500

    transaction_response = {
        "id": new_transaction.id,
        "truck": new_transaction.truck,
        "bruto": new_transaction.bruto
    }
    if direction == "out":
        transaction_response["truckTara"] = new_transaction.truckTara
        transaction_response["neto"] = new_transaction.neto or "na"

    logger.info("Transaction creation request processed successfully")
    return transaction_response, 201
