from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_USER=os.environ.get('DATABASE_USER')
DATABASE_NAME=os.environ.get('DATABASE_NAME')
DATABASE_PASSWORD=os.environ.get('DATABASE_PASSWORD')
HOST=os.environ.get('HOST')
PORT=int(os.environ.get('PORT'))

# Create the Flask application instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}"
db = SQLAlchemy(app)
# Define a route for the root URL ("/") to return "Hello, World!"
@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
