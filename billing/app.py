from datetime import datetime
import os
from uuid import uuid4

from flask import (
    Flask,
    jsonify,
    render_template,
    redirect,
    request,
    send_file,
    url_for,
    send_file,
)
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from . import db, app, logger
from app.models import Truck, Rate, Provider
from app.utilities.app_utility import add_rates_to_rates_db, delete_prev_rates_file


# from models.truck import Truck

logger.info("Initializing Flask app")



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
    truck_data = [
        {"id": truck.id, "provider_id": truck.provider_id} for truck in trucks
    ]
    return jsonify(truck_data)


@app.route("/provider")
def get_providers():
    logger.info("in provider")
    providers = Provider.query.all()
    provider_data = [
        {"id": provider.id, "name": provider.name} for provider in providers
    ]
    return jsonify(provider_data)


@app.route("/truck/<id>/", methods=["GET"])  # could be extended to other methods
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
trucks = {}


@app.route("/provider", methods=["POST"])
def post_provider():
    try:
        # Get the new name from the request body
        data = request.get_json()
        name = data.get("name")

        provider = Provider.query.filter_by(name=name).first()
        logger.info(f"provider: {provider}")

        # Check if name exists
        if provider is None:
            new_provider = Provider(name=name)  # Create new provider instance

            # Add the new provider instance to the session
            db.session.add(new_provider)

            db.session.commit()
            logger.info(f"New provider with ID {new_provider.id} created successfully.")

            # Return a successful response with the new provider ID
            return jsonify(
                {"message": f"Provider created successfully. ID: {new_provider.id}"},
                201,
            )

        # If name already exists, return appropriate error response
        logger.warning(f"Name: {name} already exists")
        return jsonify({"error": f"Provider name: {name} already exists"}), 409

    except Exception as e:
        logger.error(f"Error creating new provider: {e}")
        db.session.rollback()  # Rollback changes in case of errors
        return jsonify({"error": "Internal server error"}), 500


@app.route("/provider/<string:provider_id>", methods=["PUT"])
def update_provider(provider_id):
    # Check if the provider exists in the dictionary using its GUID
    if provider_id not in providers:
        return jsonify({"message": "Provider not found"}), 404

    # Get the new name from the request body
    data = request.get_json()
    new_name = data.get("name")

    # Validate the new name
    if not new_name:
        return jsonify({"message": "No name provided"}), 400

    # Update the provider's name
    providers[provider_id]["name"] = new_name

    # Return the updated provider info
    return (
        jsonify(
            {
                "message": "Provider updated successfully",
                "provider": providers[provider_id],
            }
        ),
        200,
    )


# POST /truck
# registers a truck in the system
# - provider - known provider id
# - id - the truck license plate


@app.route("/truck", methods=["POST"])
def register_truck():
    data = request.get_json()
    provider_id = data.get("provider")
    truck_id = data.get("id")  # Assuming truck ID is the license plate
    if not provider_id or not truck_id:
        return (
            jsonify(
                {"message": "Both provider ID and truck license plate must be provided"}
            ),
            400,
        )
    if provider_id not in providers:
        return jsonify({"message": "Provider ID does not exist"}), 404
    if truck_id in trucks:
        return jsonify({"message": "Truck ID must be unique"}), 400
    trucks[truck_id] = {"provider": provider_id}
    return (
        jsonify({"message": "Truck registered successfully", "truckId": truck_id}),
        201,
    )


@app.route("/rates", methods=["POST"])
def upload_new_rates():
    # Check if the request contains the file field
    if "file" not in request.form:
        return "No file path provided in the request", 400

    file_path = os.path.join("/app/rates_files", request.form["file"])

    try:
        df = pd.read_excel(file_path)

        # Check if the required columns are present
        required_columns = ["Product", "Rate", "Scope"]
        if not set(required_columns).issubset(df.columns):
            return f"Missing required columns: {', '.join(required_columns)}", 400

        # Create a list to store updates
        updates = []

        # Iterate over rows and collect updates
        for index, row in df.iterrows():
            product_id = row["Product"]
            rate = row["Rate"]
            scope = row["Scope"]

            if scope == "All":
                provider_id = scope

            elif isinstance(int(scope), int):
                provider_id = scope
                provider = Provider.query.get(provider_id)
                if provider is None:
                    return (
                        f"Provider with id {provider_id} does not exist. File was not saved, No changes were made to the database",
                        400,
                    )
                provider_id = provider.id
            else:
                return (
                    "Invalid value for 'Scope'. It should be 'ALL' or a provider id. File was not saved, no change to db",
                    400,
                )

            # Collect updates
            updates.append(
                {"product_id": product_id, "rate": rate, "scope": provider_id}
            )

        add_rates_to_rates_db(updates)

        in_directory = "/app/in"
        delete_prev_rates_file(in_directory)

        # Save the new file in the /in directory
        df.to_excel(os.path.join(in_directory, "rates.xlsx"), index=False)

        return "Rates uploaded successfully", 200

    except Exception as e:
        db.session.rollback()
        return (
            f"Error reading or saving Excel file: {e}. No changes were made to the database",
            400,
        )


@app.route("/rates", methods=["GET"])
def download_new_rates():
    try:

        # Path to the file to be downloaded
        file_path = "/app/in/rates.xlsx"

        # Check if the file exists
        if not os.path.exists(file_path):
            return "No rates file uploded yet", 404

        # Send the file for download
        return send_file(file_path, as_attachment=True)

    except Exception as e:
        return f"Error downloading file: {e}", 500




#  return 'Message posted successfully'
print("test if being ran")

