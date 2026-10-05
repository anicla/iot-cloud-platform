import datetime
import os

import requests
from flask import Flask, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


def service_url(address_var, port_var, path):
    host = os.getenv(address_var)
    port = os.getenv(port_var)
    return f"http://{host}:{port}{path}"


@app.route("/containers/", methods=["GET"])
@app.route("/containers/active/", methods=["GET"])
def get_containers():
    devices_response = requests.get(service_url("DEVICES_MICROSERVICE_ADDRESS", "DEVICES_MICROSERVICE_PORT", "/containers/sessions/"))
    if devices_response.status_code >= 300:
        return devices_response.json(), devices_response.status_code
    positions_response = requests.get(service_url("TELEMETRY_MICROSERVICE_ADDRESS", "TELEMETRY_MICROSERVICE_PORT", "/telemetry/positions/"))
    return positions_response.json(), positions_response.status_code


@app.route("/containers/telemetry/", methods=["GET"])
def get_container_telemetry():
    container_id = request.args.get("container_id")
    end_interval = datetime.datetime.now()
    init_interval = end_interval - datetime.timedelta(minutes=1)
    params = {
        "container_id": container_id,
        "init_interval": init_interval.isoformat(),
        "end_interval": end_interval.isoformat(),
    }
    response = requests.get(
        service_url("TELEMETRY_MICROSERVICE_ADDRESS", "TELEMETRY_MICROSERVICE_PORT", "/telemetry/"),
        json=params,
    )
    return response.json(), response.status_code


@app.route("/containers/config/", methods=["GET"])
def get_container_config():
    params = {"container_id": request.args.get("container_id")}
    response = requests.get(
        service_url("DEVICES_MICROSERVICE_ADDRESS", "DEVICES_MICROSERVICE_PORT", "/containers/config/"),
        json=params,
    )
    return response.json(), response.status_code


@app.route("/containers/config/", methods=["POST"])
def update_container_config():
    data = request.get_json(silent=True) or request.form.to_dict()
    payload = {
        "container_id": data.get("container_id"),
        "sampling": data.get("sampling"),
        "rate": data.get("rate"),
    }
    response = requests.post(
        service_url("DEVICES_MICROSERVICE_ADDRESS", "DEVICES_MICROSERVICE_PORT", "/containers/config/"),
        json=payload,
    )
    return response.json(), response.status_code


if __name__ == "__main__":
    app.run(host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", "5003")))

