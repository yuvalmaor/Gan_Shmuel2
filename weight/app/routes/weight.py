from flask import Flask, request, jsonify, Blueprint
from datetime import datetime

weight_blueprint = Blueprint('weight_blueprint', __name__)

@weight_blueprint.route('/weight', methods=['GET'])
def get_weights():
    from_date_str = request.args.get('from', datetime.now().strftime('%Y%m%d') + '000000')
    to_date_str = request.args.get('to', datetime.now().strftime('%Y%m%d%H%M%S'))
    filter_directions = request.args.get('filter', 'in,out,none').split(',')

    from_date = datetime.strptime(from_date_str, '%Y%m%d%H%M%S')
    to_date = datetime.strptime(to_date_str, '%Y%m%d%H%M%S')

    #database queries

    response = [{
        "ID": 1,
        "direction": "in",
        "bruto": 20000,
        "neto": 19500,
        "produce": "Appels",
        "containers": ["C1","C2","C3"]
    }]

    return jsonify(response), 200