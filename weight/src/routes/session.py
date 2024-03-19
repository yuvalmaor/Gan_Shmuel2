from flask import jsonify, Blueprint
from ..models import Transaction
from ..config import logger

session_blueprint = Blueprint('session_blueprint', __name__)


@session_blueprint.route('/session/<id>', methods=['GET'])
def get_session(id):
    logger.info("Received request to Find A Specific Weighing Session")

    try:
        logger.info("Retrieving Weighing Session from database")
        session_transactions = Transaction.query.filter(
            Transaction.session_id == id).all()
    except:
        logger.error("An error occurred while querying the database")
        return jsonify({"error": "An error occurred while querying the database"}), 500

    if not session_transactions:
        logger.info("Session not found")
        return jsonify({"error": "Session not found"}), 404

    response = {
        "id": id,
        "truck": getattr(session_transactions[0], "truck", "na"),
        "bruto": session_transactions[0].bruto,
    }

    for trans in session_transactions:
        if trans.direction == 'out':
            response["truckTara"] = trans.truckTara
            response["neto"] = getattr(trans, "neto", "na")

    logger.info(f"Returnig session {id}")
    return jsonify(response), 200
