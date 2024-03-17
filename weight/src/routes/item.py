from flask import request, jsonify, Blueprint
from datetime import datetime

# Import necessary database models and configurations
from ..models import Transaction, Container
from ..config import logger
from ..database import db


# Create a blueprint for handling item-related routes
item_blueprint = Blueprint('item_blueprint', __name__)

# Define a route to handle GET requests for retrieving item information by ID
@item_blueprint.route('/item/<id>', methods=['GET'])
def get_item(id):

    # Log that a request to find an item has been received
    logger.info("Received request to Find an Item")
    
     # Query the Container table for the given ID & Query the Transaction table for trucks associated with the given ID (ID can represent Either Transactio or Container)
    container = Container.query.filter_by(container_id=id).first()
    truck = Transaction.query.filter_by(truck=id).all()
    
    
    # If neither a container nor a truck is found with the given ID, return an error response
    if not container and not truck:
        return jsonify({"error": "Item not found"}), 404
    
     # Define default start and end dates for filtering transactions
    default_from = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    default_to = datetime.now()
    
    # Parse 'from' and 'to' date parameters from the request URL
    from_date_str = request.args.get('from', datetime.now().strftime('%Y%m%d') + '000000', default_from)
    to_date_str = request.args.get('to', datetime.now().strftime('%Y%m%d%H%M%S'), default_to)
    
    # Convert 'from' and 'to' date strings to datetime objects
    try:
        from_date = datetime.strptime(from_date_str, '%Y%m%d%H%M%S') 
        to_date = datetime.strptime(to_date_str, '%Y%m%d%H%M%S')
    except ValueError:
        # Return an error response if the date format is invalid
        return jsonify({"error": "Invalid date-time format"}), 400
    

    item = {"id":id,"tara":"na"}

    # Initialize item dictionary with basic information
    if not truck:
        container_transactions=Transaction.query.all()
        container_sessions=list(filter(lambda x: container.container_id in x.containers.split(','),container_transactions))
        container_sessions = set(map(lambda x: x.session_id, container_sessions))
        item["sessions"]=list(container_sessions)

    else:
        # If a truck is associated with the given ID, retrieve truck sessions
        truck_sessions = list(map(lambda x: x.session_id, truck))
        item["id"]=truck["truck"]
        item["tara"]=truck["truckTara"],
        item["sessions"]=truck_sessions
        
    # Return the item information in JSON format
    return jsonify(item)