from flask import request, jsonify, Blueprint
from datetime import datetime

# Import necessary database models and configurations
from ..models import Transaction
from ..config import logger

# Create a blueprint for handling item-related routes
item_blueprint = Blueprint('item_blueprint', __name__)

# Define a route to handle GET requests for retrieving item information by ID
@item_blueprint.route('/item/<id>', methods=['GET'])
def get_item(id):
    try:
        # Log that a request to find an item has been received
        logger.info(f"Received request to Find an Item, id: {id}")
        # Define default start and end dates for filtering transactions
        default_from_str = datetime.now().replace(day=1, hour=0, minute=0, second=0,
                                                microsecond=0).strftime('%Y%m%d%H%M%S')
        default_to_str = datetime.now().strftime('%Y%m%d%H%M%S')
        # Parse 'from' and 'to' date parameters from the request URL
        from_date_str = request.args.get('from', default_from_str)
        to_date_str = request.args.get('to', default_to_str)
        # Convert 'from' and 'to' date strings to datetime objects
        try:
            from_date = datetime.strptime(from_date_str, '%Y%m%d%H%M%S')
            to_date = datetime.strptime(to_date_str, '%Y%m%d%H%M%S')
        except ValueError:
            # Return an error response if the date format is invalid
            return jsonify({"error": "Invalid date-time format"}), 400
        TRANSACTIONS = []
        ID_IS_TRUCK=False
        try:
            #PULLING ALL THE TRANSACTIONS AND CHECK IF THERE IS A TRUCK THAT MATCHES THE ID
            TRANSACTIONS = Transaction.query.filter(
                Transaction.datetime >= from_date,
                Transaction.datetime <= to_date).order_by(Transaction.id.desc()).all()
            #IF THERE IS A MATCH THEN WE TURN THE FLAG INTO TRUE WHICH MEANS (THE INPUTED ID REFERS TO A TRUCK)
            logger.info(f"transactions: {TRANSACTIONS}")
            ID_IS_TRUCK = any(trans.truck == id for trans in TRANSACTIONS)
        except:
            return jsonify({"error": "Cannot access database"}), 500
        response = {"id": id, "tara": "na"}
        if ID_IS_TRUCK:
            
            #ITEM_IS_A_TRUCK RESPONSE GENERATING
            TRUCK_SESSIONS = set(map(lambda x: x.session_id, filter(lambda x: x.truck == id, TRANSACTIONS)))
            response["sessions"] = list(TRUCK_SESSIONS)
            response["tara"] = next((transaction.truckTara for transaction in TRANSACTIONS if transaction.truckTara != None and transaction.truck == id), None)
            return jsonify(response),200
        else:
            #SEARCHING IF THE ITEM ID REFERS TO A CONTAINER
            CONTAINER_TRANSACTIONS = []
            for trans in TRANSACTIONS:
                if trans.containers == id and trans.containers != 'na' and trans.containers != '':
                    CONTAINER_TRANSACTIONS.append(trans)
                    continue
                for str in trans.containers.split(','):
                    if str == id and str != '' and str != 'na':
                        CONTAINER_TRANSACTIONS.append(trans)
                        break
            #WASN'T_FOUND_IN_ANY_TRANSACTION_RECORD
            if len(CONTAINER_TRANSACTIONS) == 0:
                return jsonify({"error": "This Id has 0 transactions matched"}), 404
            #ITEM_IS_A_CONTAINER GENERATING THE RESPONSE MESSAGE   
            given_container_sessions = list(set(map(lambda x: x.session_id, CONTAINER_TRANSACTIONS)))
            response["sessions"]=given_container_sessions
            return jsonify(response),200
        #ITEM_ISN'T_A_CONTAINER_OR_A_TRUCK
        return jsonify({"error": "Item not found"}), 404
    except Exception as e:
         logger.info(e)
         return e