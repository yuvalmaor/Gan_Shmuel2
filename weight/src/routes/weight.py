from flask import Flask, request, jsonify, Blueprint
from datetime import datetime
from ..models import Transaction

weight_blueprint = Blueprint('weight_blueprint', __name__)

@weight_blueprint.route('/weight', methods=['GET'])
def get_weights():
    from_date_str = request.args.get('from', datetime.now().strftime('%Y%m%d') + '000000')
    to_date_str = request.args.get('to', datetime.now().strftime('%Y%m%d%H%M%S'))
    filter_directions = request.args.get('filter', 'in,out,none').replace('"', '').split(',')

    from_date = datetime.strptime(from_date_str, '%Y%m%d%H%M%S')
    to_date = datetime.strptime(to_date_str, '%Y%m%d%H%M%S')

    #database queries

    transactions = Transaction.query.filter(
        Transaction.datetime >= from_date,
        Transaction.datetime <= to_date,
        Transaction.direction.in_(filter_directions)
    ).all()

    response = [{
        "ID": transaction.id,
        "direction": transaction.direction,
        "bruto": transaction.bruto,
        "neto": transaction.neto if transaction.neto is not None else "na",
        "produce": transaction.produce,
        "containers": transaction.containers.split(',') if transaction.containers else [],
        "session_id": transaction.session_id
    } for transaction in transactions]

    return jsonify(response), 200