from flask import Flask
from .config import Config
from .database import db
from .routes import weight, health , session , item , unkown, batch


def create_app(database_uri=''):
    # Create the Flask application instance
    app = Flask(__name__)

    #config
    app.config.from_object(Config)
    if database_uri:
        app.config["SQLALCHEMY_DATABASE_URI"] = database_uri

    #routes
    app.register_blueprint(weight.weight_blueprint)
    app.register_blueprint(health.health_blueprint)
    app.register_blueprint(batch.batch_blueprint)
    app.register_blueprint(session.session_blueprint)
    app.register_blueprint(unkown.unknown_blueprint)
    app.register_blueprint(item.item_blueprint)

    db.init_app(app)
    return app
