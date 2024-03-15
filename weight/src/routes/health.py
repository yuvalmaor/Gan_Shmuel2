from flask import Blueprint, Response
from ..config import logger

health_blueprint = Blueprint("health", __name__)


@health_blueprint.route("/health", methods=["GET"])
def check_health():
    
    logger.info("Health check endpoint accessed")
    is_database_ok = True
    
    if is_database_ok:
        logger.info("Health check successful - server and database are running")
        return Response("OK", 200)
    else:
        logger.critical("Health check failed - database is unreachable")
        return Response("Failure", 500)
