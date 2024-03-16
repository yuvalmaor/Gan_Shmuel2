
from flask import Flask, request, jsonify

# TODO: import models once they've been created properly(Truck, Provider, Rate)
# from app.models.chat import Truck, Provider, Rate

# TODO: if desired, we could add every truck rest into this function, for now it's only for the "GET"
# @app.route("/truck/<id>/", methods=['GET']) # could be extended to other methods
# def truckREST(id):
#     print("in truckREST")
#     # Check if the truck exists
#     if id not in trucks:
#         return jsonify({"error": "Truck not found"}), 404

#       # Set default t1 and t2
#     t1_default = "01000000"  # 1st of month at 00:00:00
#     t2_default = "now"  # Assuming "now" means the current time

#     t1 = request.args.get("from", t1_default)
#     t2 = request.args.get("to", t2_default)

#      # Here you may want to convert t1 and t2 to proper datetime objects
#     # For simplicity, let's just print them for now
#     print("t1:", t1)
#     print("t2:", t2)

#     response_json = {
#         "id": trucks[id]["id"],
#         # "tara": trucks[id]["tara"],
#         # "sessions": trucks[id]["sessions"]
#     }

#     # Return json
#     return jsonify(response_json), 200
