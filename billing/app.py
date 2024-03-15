from datetime import datetime
import os
from uuid import uuid4
from flask import Flask, jsonify, render_template, redirect, request, send_file, url_for
from flask_sqlalchemy import SQLAlchemy
from app import logger

logger.info('Initializing Flask app')
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:1234@mysql/billdb"  # Note the database name change to 'billdb'

db = SQLAlchemy(app)

# Define SQLAlchemy models
class Provider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

class Rate(db.Model):
    __tablename__ = 'Rates'  # Specify the table name explicitly to match the schema
    product_id = db.Column(db.String(50), primary_key=True)
    rate = db.Column(db.Integer, default=0)
    scope = db.Column(db.String(50), db.ForeignKey('provider.id'))
    provider = db.relationship('Provider', backref='rates')

class Truck(db.Model):
    __tablename__ = 'Trucks'  # Specify the table name explicitly to match the schema
    id = db.Column(db.String(10), primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'))
    provider = db.relationship('Provider', backref='trucks')


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
    logger.info(f"in /truck/<id>/:")
    trucks = Truck.query.all()
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

     # Here you may want to convert t1 and t2 to proper datetime objects
    # For simplicity, let's just print them for now
    print("t1:", t1)
    print("t2:", t2)


    truck_data = {
        "id": truck.id,
        "provider_id": truck.provider_id
        # "tara": trucks[id]["tara"], 
        # "sessions": trucks[id]["sessions"]
    }


    logger.info(f"Found trucksies: {truck_data}")
    # Return json
    return jsonify(truck_data), 200

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
print (f"__name__: {__name__}")
if __name__ == "__app.app__":
    print("Starting Flask application...")
    app.run(debug=True)