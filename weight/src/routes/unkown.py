from flask import request, jsonify, Blueprint
from datetime import datetime

from pymysql import NULL
from ..models import Transaction, Container
from ..config import logger
from ..database import db

unknown_blueprint = Blueprint('unknown_blueprint', __name__)

@unknown_blueprint.route('/unknown', methods=['GET'])
def find_truck_or_container():
    
    logger.info("Received request to Find Unknown Weight Transactions")
    
    # Fetch unweighted containers from the database
    try:
        unweighted_containers = Container.query.filter(Container.weight == None).all()
    except Exception as e:
        return jsonify({"error": "An error occurred while querying the database: {}".format(str(e))}), 500

    logger.info("Returning Unweighted Containers IDs")
    
    # Collect the IDs of unweighted containers as strings
    container_ids = [str(container.id) for container in unweighted_containers]

    
    return jsonify(container_ids), 200