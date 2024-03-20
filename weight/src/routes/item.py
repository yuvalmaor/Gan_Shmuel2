from flask import request, jsonify, Blueprint
from datetime import datetime

# Import necessary database models and configurations
from ..models import Transaction, Container
from ..config import logger


# Create a blueprint for handling item-related routes
item_blueprint = Blueprint('item_blueprint', __name__)

# Define a route to handle GET requests for retrieving item information by ID


@item_blueprint.route('/item/<id>', methods=['GET'])
def get_item(id):

    # Log that a request to find an item has been received
    logger.info("Received request to Find an Item")

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

    # Query the Container table for the given ID & Query the Transaction table for trucks associated with the given ID (ID can represent Either Transactio or Container)
    container_transactions = []
    truck_transactions = []
    try:
        container_transactions = Transaction.query.filter(
            Transaction.direction == 'none',
            Transaction.containers == id,
            Transaction.datetime >= from_date,
            Transaction.datetime <= to_date).all()

        truck_transactions = Transaction.query.filter(
            Transaction.truck == id,
            Transaction.datetime >= from_date,
            Transaction.datetime <= to_date).all()
    except:
        return jsonify({"error": "Cannot access database"}), 500

    # If neither a container nor a truck is found with the given ID, return an error response
    transactions_trucks_with_container = []
    if not truck_transactions:
        try:
            transactions_trucks_with_container = Transaction.query.filter(
                Transaction.datetime >= from_date,
                Transaction.datetime <= to_date,
                Transaction.containers.like(f"%{id}%")
            ).all()
            if not transactions_trucks_with_container:
                return jsonify({"error": "Item not found"}), 404
        except:
            return jsonify({"error": "Cannot access database"}), 500

    # Initialize item dictionary with basic information
    item = {"id": id, "tara": "na"}

    if not truck_transactions:
        container_sessions = set(map(lambda x: x.session_id, transactions_trucks_with_container)) | \
            set(map(lambda x: x.session_id, container_transactions))
        item["sessions"] = list(container_sessions)
    else:
        # If a truck is associated with the given ID, retrieve truck sessions
        truck_sessions = set(map(lambda x: x.session_id, truck_transactions))
        item["sessions"] = list(truck_sessions)

        last_numeric_tara = next((x for x in reversed(list(map(
            lambda x: x.truckTara, truck_transactions))) if x is not None and isinstance(x, (int))), 'na')
        item["tara"] = last_numeric_tara

    # Return the item information in JSON format
    return jsonify(item), 200
