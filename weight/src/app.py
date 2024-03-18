from flask import Flask
from .config import Config
from .database import db
from .routes import weight, health , session , item , unkown, batch

# Create the Flask application instance
app = Flask(__name__)

#config
app.config.from_object(Config)

#routes
app.register_blueprint(weight.weight_blueprint)
app.register_blueprint(health.health_blueprint)
app.register_blueprint(batch.batch_blueprint)
app.register_blueprint(session.session_blueprint)
app.register_blueprint(unkown.unknown_blueprint)
app.register_blueprint(item.item_blueprint)
# Define a route for the root URL ("/") to return "Hello, World!"
@app.route('/')
def hello_world():
    return 'Hello, World!'

db.init_app(app)
