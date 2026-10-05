import os

from flask import Flask, request
from flask_cors import CORS

from telemetry_db_manager import query_telemetry, register_new_telemetry, retrieve_containers_last_position


app = Flask(__name__)
CORS(app)


@app.route("/telemetry/", methods=["POST"])
def register_telemetry():
    data = request.get_json()
    if register_new_telemetry(data):
        return {"result": "Telemetry registered"}, 201
    return {"result": "Error registering telemetries"}, 500


@app.route("/telemetry/", methods=["GET"])
def get_telemetry():
    params = request.get_json(silent=True) or request.args.to_dict()
    return query_telemetry(params), 200


@app.route("/telemetry/positions/", methods=["GET"])
def get_containers_last_position():
    error_message, result = retrieve_containers_last_position()
    if error_message == "":
        return result, 200
    return {"Error Message": error_message}, 500


if __name__ == "__main__":
    app.run(host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", "5001")))

