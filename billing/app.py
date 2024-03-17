from datetime import datetime
import os
from uuid import uuid4
from flask import Flask, jsonify, render_template, redirect,  request, send_file, url_for
import requests
from . import db, app, logger
import unittest
from flask_sqlalchemy import SQLAlchemy
from app.models import Truck, Rate, Provider

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


@app.route("/truck/<id>/", methods=['GET']) # could be extended to other methods
def truckREST(id):
    try:
        logger.info(f"in truckREST: {truckREST}")
        # trucks = Truck.query.all()
        truck: int = Truck.query.filter_by(id=id).first()
        # Check if the truck exists
        if truck is None:
            logger.warning(f"Truck with ID {id} not found")
            return jsonify({"error": f"Truck with ID {id} not found"}), 404

        # Set default t1 and t2
        t1_default: str = "01000000"  # 1st of month at 00:00:00
        t2_default: str = "now"  # Assuming "now" means the current time

        t1: str = request.args.get("from", t1_default)
        t2: str = request.args.get("to", t2_default)

        # Here you may want to convert t1 and t2 to proper datetime objects
        # For simplicity, let's just print them for now

        logger.info(f"after setting default - t1: {t1}, t2: {t2}")

        # Make the GET request to the third-party API
        url = f"https://weight2/item/{id}?from={t1}&to={t2}"
        response = requests.get(url)

        if response.status_code == 404:
            return jsonify({"error": f"Truck with ID {id} not found"}), 404
        elif response.status_code != 200:
            return jsonify({"error": "Failed to retrieve truck data"}), response.status_code
        truck_data: dict[str,str] = response.json()
        logger.info(f"Found truck_data: {truck_data}")
    
        # Return json
        return jsonify(truck_data), 200
    # TODO: check connectivity before or after

    except Exception as e:
        logger.error(f"An exception occurred: {e}")
        return e.status_code

# In-memory storage for simplicity (replace with database later)
providers = {}


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



#     return 'Message posted successfully'
print("test if being ran")

print (f"__name__ inside app.py: {__name__}")
if __name__ == "__app__":
    print("Starting Flask application...")
    app.run(debug=True)
    # unittest.main()

# from app.models import routes