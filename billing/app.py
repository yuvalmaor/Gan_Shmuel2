from datetime import datetime
import os
from flask import Flask, jsonify, render_template, redirect, request, send_file, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@mysql/chat'

db = SQLAlchemy(app)

# class Message(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(100), nullable=False)
#     message = db.Column(db.Text, nullable=False)
#     date = db.Column(db.Date, nullable=False)
#     time = db.Column(db.Time, nullable=False)
#     room = db.Column(db.String(100), nullable=False)

# # Create database tables before running the application
# with app.app_context():
#     db.create_all()

@app.route("/")
def home():
    print("home function")
    return "Hellooooo"



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
