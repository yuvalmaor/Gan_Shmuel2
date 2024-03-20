
from flask import jsonify, Blueprint
from ..config import logger

session_blueprint = Blueprint('session_blueprint', __name__)

logs_blueprint = Blueprint("logs",__name__)

@logs_blueprint.route("/logs", methods=["GET"])
def get_logs():
    res = ""
    try:
        with open("./logs/weight-logs.txt", "r") as file:
            res = file.readlines()
        return res, 200
    except FileNotFoundError:
        return {"Error": "No log file"}, 500
