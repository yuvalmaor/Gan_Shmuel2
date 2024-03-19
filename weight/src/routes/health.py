from flask import Blueprint, Response
from ..config import logger
from ..database import db
from sqlalchemy import text

health_blueprint = Blueprint("health", __name__)


@health_blueprint.route("/health", methods=["GET"])
def check_health():
    logger.info("Health check endpoint accessed")
    try:
#        db.session.execute(text("SELECT 1"))
 #       logger.info("Health check successful - server and database are running")
        return Response("OK", 200)
    except Exception as e:
        logger.critical("Health check failed - database is unreachable")
        return Response("Failure", 500)
        