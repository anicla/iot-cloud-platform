import os

import requests
from flask import Flask, request
from flask_cors import CORS

from devices_db_manager import (
    register_container_connection,
    register_container_disconnection,
    retrieve_active_containers,
    retrieve_container,
    retrieve_containers,
    save_container_config,
)


app = Flask(__name__)
CORS(app)


@app.route("/containers/", methods=["GET"])
def get_containers():
    return retrieve_containers(), 200


@app.route("/containers/sessions/", methods=["GET"])
def get_active_containers():
    return retrieve_active_containers(), 200


@app.route("/containers/sessions/", methods=["PUT"])
def connect_container():
    result = register_container_connection(request.get_json())
    if result:
        return result, 201
    return {"container_id": "", "Message": "Session connection could not be registered"}, 500


@app.route("/containers/sessions/", methods=["POST"])
def disconnect_container():
    result = register_container_disconnection(request.get_json())
    if result:
        return result, 201
    return {"container_id": "", "Message": "Session disconnection could not be registered"}, 500


@app.route("/containers/config/", methods=["GET"])
def get_config():
    params = request.get_json(silent=True) or request.args.to_dict()
    result = retrieve_container(params)
    if result:
        return result, 200
    return {"result": "Error: Container not found"}, 500


@app.route("/containers/config/", methods=["POST"])
def save_config():
    data = request.get_json(silent=True) or request.form.to_dict()
    configuration = save_container_config(data)
    if not configuration:
        return {"result": "Error: Container params not updated"}, 500
    host = os.getenv("MESSAGE_ROUTER_ADDRESS")
    port = os.getenv("MESSAGE_ROUTER_PORT")
    if host and port:
        response = requests.post(f"http://{host}:{port}/containers/config/", json=configuration)
        if response.status_code >= 300:
            return {"result": "Error: Container params not sent"}, 500
    return {"result": "Success: Container params updated"}, 200


if __name__ == "__main__":
    app.run(host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", "5002")))

