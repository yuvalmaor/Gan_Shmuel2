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
from app.utilities.app_utility import add_rates_to_rates_db, delete_prev_rates_file
from app.models import Truck, Rate, Provider
import requests

weightAdress: str = "weight-api-1"  # TODO: move to env.

@app.route("/health")
def healthcheck():
    status = {"status": "ok", "message": "Service is healthy"}
    return jsonify(status), 200


@app.route("/truck/<id>/", methods=["GET"])
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
        logger.error(
            f"Failed to retrieve truck data for ID: {id}. Status code: {response.status_code}"
        )
        return jsonify({"error": "Failed to retrieve truck data"}), response.status_code

    truck_data = response.json()
    logger.info(f"Received truck data: {truck_data}")
    return jsonify(truck_data), 200


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
    
@app.route("/provider/<provider_id>", methods=["PUT"])
def update_provider(provider_id):
    # Check if the provider exists in the database using its ID
    provider = Provider.query.get(provider_id)
    if not provider:
        return jsonify({"message": "Provider not found"}), 404
    
    # Get the new name from the request body
    data = request.get_json()
    new_name = data.get("name")

    # Validate the new name
    if not new_name:
        return jsonify({"message": "No name provided"}), 400
    
    # Update the provider's name
    provider.name = new_name
    
    # Commit the changes to the database
    db.session.commit()

    # Return the updated provider info
    return jsonify({"message": "Provider updated successfully"}), 200


from sqlalchemy.exc import IntegrityError

@app.route("/truck", methods=["POST"])
def register_truck():
    data = request.json
    # Check if all required fields are present in the request
    if "provider" not in data or "id" not in data:
        return jsonify({"message": "Missing required fields. Truck not saved."}), 400

    try:
        # Extract data from the request
        provider_id = int(data["provider"])

        truck_id = str(data["id"])  # Convert id to string

        # Check if the provider with the given ID exists
        provider = Provider.query.get(provider_id)
        if not provider:
            return jsonify({"message": f"Provider with ID {provider_id} does not exist. Truck not saved."}), 404

        # Add the truck to the database
        new_truck = Truck(id=truck_id, provider_id=provider_id)
        db.session.add(new_truck)
        db.session.commit()
    except ValueError:
        return jsonify({"message": "Truck ID must be an integer."}), 400
    except IntegrityError:
        return jsonify({"message": f"Truck with ID {truck_id} already exists in the database."}), 400
    except Exception as e:
        return jsonify({"message": f"Error saving truck to db: {e}"}), 400

    # Return a success message
    return jsonify({"message": f"Truck with ID {truck_id} registered successfully."}), 201



@app.route("/truck/<truck_id>", methods=["PUT"])
def update_truck_provider(truck_id):
    data = request.json
    
    # Check if the request contains the provider field
    if "provider" not in data:
        return jsonify({"message": "No provider ID provided in the request."}), 400

    try:
        # Extract the new provider ID from the request and convert it to a string
        new_provider_id = str(data["provider"])
        
        # Check if the truck with the given ID exists in the database
        truck = Truck.query.get(truck_id)
        if not truck:
            return jsonify({"message": f"Truck with ID {truck_id} not found."}), 404

        # Check if the provider with the new ID exists
        new_provider = Provider.query.get(new_provider_id)
        if not new_provider:
            return jsonify({"message": f"Provider with ID {new_provider_id} not found."}), 404

        # Update the provider ID for the truck
        truck.provider_id = new_provider_id
        db.session.commit()
    except ValueError:
        return jsonify({"message": "Provider ID must be a string."}), 400
    except Exception as e:
        return jsonify({"message": f"Error updating truck provider: {e}"}), 500

    return jsonify({"message": f"Provider ID for truck {truck_id} updated successfully."}), 200


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


# @app.route("/bill/<id>", methods=["GET"])
# def get_bill(id):
#     provider = Provider.query.get(id)
#     if provider is None:
#         return "wrong provider id", 400
#     now = datetime.now()
#     from_default = now.strftime("%Y%m") + "01000000"
#     to_default = now.strftime("%Y%m%d%H%M%S")
#     from_arg = request.args.get("from")
#     if not from_arg:
#         from_arg = from_default
#     else:
#         if len(from_arg) != 14:
#             return "wrong datetime value"
#         try:
#             datetime(
#                 from_arg[0:4],
#                 from_arg[4:6],
#                 from_arg[6:8],
#                 from_arg[8:10],
#                 from_arg[10:12],
#                 from_arg[12:14],
#             )
#         except ValueError:
#             return "wrong datetime value"
#     to_arg = request.args.get("to")
#     if not to_arg:
#         to_arg = to_default
#     else:
#         if len(to_arg) != 14:
#             return "wrong datetime value"
#         try:
#             datetime(
#                 to_arg[0:4],
#                 to_arg[4:6],
#                 to_arg[6:8],
#                 to_arg[8:10],
#                 to_arg[10:12],
#                 to_arg[12:14],
#             )
#         except ValueError:
#             return "wrong datetime value"
#     # get all trucks of provider id
#     trucks = Truck.query.filter_by(provider_id=provider.id).all()
#     truckCounter = 0
#     sessionCounter = 0
#     sessions = []
#     for truck in trucks:
#         truck_id = truck.truck_id
#         WEIGHT__URI = f"http://{SERVER}:8084/"
#         response = requests.get(
#             WEIGHT_URI + f"/{truck_id}", params={"from": from_arg, "to": to_arg}
#         )
#         response.raise_for_status()
#         truck_sessions = response.json()["sessions"]
