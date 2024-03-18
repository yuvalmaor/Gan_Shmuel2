from datetime import datetime
import os
from uuid import uuid4
from flask import Flask, jsonify, render_template, redirect, request, send_file, url_for
from flask_sqlalchemy import SQLAlchemy
from . import db, app, logger
from app.models import Truck, Rate, Provider
import requests
# from models import Provider, Rate, Truck


#from models.truck import Truck

logger.info('Initializing Flask app')

@app.route("/")
def home():
    print("home function")
    return "Hellooooo"

@app.route("/health")
def healthcheck():
    
    status = {"status": "ok", "message": "Service is healthy"}
    return jsonify(status), 200



@app.route("/trucks")
def get_trucks():
    logger.info("in trucks")
    trucks = Truck.query.all()
    truck_data = [{"id": truck.id, "provider_id": truck.provider_id} for truck in trucks]
    return jsonify(truck_data)


weightAdress:str = "weight-api-1" # TODO: move to env.
@app.route("/truck/<id>/", methods=['GET'])
def truckREST(id):
    logger.info(f"Received GET request for truck with ID: {id}")

    truck = Truck.query.filter_by(id=id).first()

    # Check if the truck exists
    if truck is None:
        logger.warning(f"Truck with ID {id} not found")
        return jsonify({"error": f"Truck with ID {id} not found"}), 404

    # Set default t1 and t2
    t1_default = "01000000"  # 1st of month at 00:00:00
    t2_default = "now"  # Assuming "now" means the current time

    t1 = request.args.get("from", t1_default)
    t2 = request.args.get("to", t2_default)

    logger.info(f"Received 'from' parameter: {t1}, 'to' parameter: {t2}")

    # Define the URL for the third-party API
    url = f"{weightAdress}/item/{id}?from={t1}&to={t2}"

    logger.info(f"Making GET request to: {url}")

    # Make the GET request to the third-party API
    response = requests.get(url)
    if response.status_code == 404:
        logger.warning(f"Truck data not found for ID: {id}")
        return jsonify({"error": f"Truck with ID {id} not found"}), 404
    elif response.status_code != 200:
        logger.error(f"Failed to retrieve truck data for ID: {id}. Status code: {response.status_code}")
        return jsonify({"error": "Failed to retrieve truck data"}), response.status_code

    truck_data = response.json()

    logger.info(f"Received truck data: {truck_data}")

    return jsonify(truck_data), 200



# In-memory storage for simplicity (replace with database later)
providers = {}
trucks = {}


@app.route("/<provider>", methods=["POST"])
def post_provider(provider):
    # Check for unique name
    if provider in providers:
        return jsonify({"error": "Provider name already exists"}), 409

    # Generate unique ID
    provider_id = uuid4().hex

    # Add provider to in-memory storage (replace with database write)
    providers[provider] = provider_id

    # Return created provider ID
    return jsonify({"id": provider_id}), 201

@app.route('/provider/<string:provider_id>', methods=['PUT'])
def update_provider(provider_id):
    # Check if the provider exists in the dictionary using its GUID
    if provider_id not in providers:
        return jsonify({'message': 'Provider not found'}), 404

    # Get the new name from the request body
    data = request.get_json()
    new_name = data.get('name')

    # Validate the new name
    if not new_name:
        return jsonify({'message': 'No name provided'}), 400

    # Update the provider's name
    providers[provider_id]['name'] = new_name

    # Return the updated provider info
    return jsonify({'message': 'Provider updated successfully', 'provider': providers[provider_id]}), 200


#POST /truck
#registers a truck in the system
#- provider - known provider id
#- id - the truck license plate


@app.route('/truck', methods=['POST'])
def register_truck():
    data = request.get_json()
    provider_id = data.get('provider')
    truck_id = data.get('id')  # Assuming truck ID is the license plate
    if not provider_id or not truck_id:
        return jsonify({'message': 'Both provider ID and truck license plate must be provided'}), 400
    if provider_id not in providers:
        return jsonify({'message': 'Provider ID does not exist'}), 404
    if truck_id in trucks:
        return jsonify({'message': 'Truck ID must be unique'}), 400
    trucks[truck_id] = {'provider': provider_id}
    return jsonify({'message': 'Truck registered successfully', 'truckId': truck_id}), 201


# from app.models import routes

#     return 'Message posted successfully'
print("test if being ran")
print (f"__name__: {__name__}")
if __name__ == "__app.app__":
    print("Starting Flask application...")
    app.run(debug=True)

