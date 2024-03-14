from datetime import datetime
import os
from uuid import uuid4
from flask import Flask, jsonify, render_template, redirect, request, send_file, url_for
from flask_sqlalchemy import SQLAlchemy

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
    trucks = Truck.query.all()
    truck_data = [{"id": truck.id, "provider_id": truck.provider_id} for truck in trucks]
    return jsonify(truck_data)



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


# @app.route('/api/chat/<room>', methods=['POST'])
# def post_message(room):
#     username = request.form['username']
#     message = request.form['msg']
#     date = datetime.now().date()
#     time = datetime.now().time()

#     # Save the message to the database
#     new_message = Message(username=username, message=message, date=date, time=time, room=room)
#     db.session.add(new_message)
#     db.session.commit()

#     return 'Message posted successfully'

if __name__ == "__main__":
    app.run(debug=True)