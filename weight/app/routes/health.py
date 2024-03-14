from flask import Blueprint, Response

health_blueprint = Blueprint("health", __name__)

@health_blueprint.route("/health", methods=["GET"])
def check_health():
    is_database_ok = True
    if is_database_ok:
        return Response("OK",200)
    else:
        return Response("Failure", 500)