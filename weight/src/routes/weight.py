from flask import request, jsonify, Blueprint
from datetime import datetime
from ..models import Transaction
from ..config import logger

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
      
    try:  
        from_date = datetime.strptime(from_date_str, '%Y%m%d%H%M%S')
        to_date = datetime.strptime(to_date_str, '%Y%m%d%H%M%S')
    except:
        return jsonify({"error": "The provided date parameters are not valid. Ensure they are in the 'YYYYMMDDHHMMSS' format and both dates are provided."})
    
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
