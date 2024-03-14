from flask import Flask
from config import Config
from database import db

# Create the Flask application instance
app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    # app.run(debug=True)
