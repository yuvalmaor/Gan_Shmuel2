from flask import request, jsonify, Blueprint
from datetime import datetime

from pymysql import NULL
from ..models import Transaction, Container
from ..config import logger
from ..database import db

session_blueprint = Blueprint('session_blueprint', __name__)

@session_blueprint.route('/session/<id>', methods=['GET'])
def get_session(id):


    logger.info("Received request to Find A Specific Weighing Session")
    
    
    session_transactions = Transaction.query.filter_by(session_id=id).all()
    
    if not session_transactions or session_transactions.count == 0:
        return jsonify({"error": "Session not found"}), 404
    
    response = { "id": id, 
            "truck": session_transactions[0].truck if session_transactions[0].truck else "na", 
            "bruto": session_transactions[0].bruto,
             }


    for trans in session_transactions:
        if trans.direction == 'out':
            response["truckTara"]=trans.truckTara
            response["neto"]=trans.neto if trans.neto else 'na'

    return jsonify(response)