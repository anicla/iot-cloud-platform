import datetime
import json
import os
import threading

import paho.mqtt.client as mqtt
import requests
from flask import Flask, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
client = mqtt.Client()


def register_device_connection(data, hostname):
    host = os.getenv("DEVICES_MICROSERVICE_ADDRESS")
    port = os.getenv("DEVICES_MICROSERVICE_PORT")
    response = requests.put(f"http://{host}:{port}/containers/sessions/", json={
        "container_id": data["Container_id"],
        "container_hostname": hostname,
    })
    return response.json() if response.status_code == 201 else {"Authorization": "False"}


def register_device_disconnection(data):
    host = os.getenv("DEVICES_MICROSERVICE_ADDRESS")
    port = os.getenv("DEVICES_MICROSERVICE_PORT")
    return requests.post(f"http://{host}:{port}/containers/sessions/", json={"container_id": data["Container_id"]})


def store_telemetry(data):
    host = os.getenv("TELEMETRY_MICROSERVICE_ADDRESS")
    port = os.getenv("TELEMETRY_MICROSERVICE_PORT")
    return requests.post(f"http://{host}:{port}/telemetry/", json=data)


def send_configuration(mqtt_client, params):
    topic = f"/fic/containers/{params['container_hostname']}/config/"
    mqtt_client.publish(topic, json.dumps(params), qos=1, retain=False)


def on_connect(mqtt_client, userdata, flags, rc):
    if rc == 0:
        mqtt_client.subscribe("/fic/containers/+/request_access/")
        mqtt_client.subscribe("/fic/containers/+/session/")


def on_message(mqtt_client, userdata, msg):
    topic = msg.topic.split("/")
    data = json.loads(msg.payload.decode())
    hostname = topic[-3]
    if "request_access" in msg.topic:
        result = register_device_connection(data, hostname)
        response = {
            "Container_id": data["Container_id"],
            "Authorization": result.get("Authorization", "True" if result else "False"),
            "Timestamp": datetime.datetime.timestamp(datetime.datetime.now()) * 1000,
        }
        mqtt_client.publish(f"/fic/containers/{hostname}/config/", json.dumps(response), qos=1)
        if response["Authorization"] == "True":
            mqtt_client.subscribe(f"/fic/containers/{hostname}/telemetry/")
    elif "telemetry" in msg.topic:
        store_telemetry(data)
    elif "session" in msg.topic:
        register_device_disconnection(data)
        mqtt_client.unsubscribe(f"/fic/containers/{hostname}/telemetry/")


@app.route("/containers/config/", methods=["POST"])
def send_params():
    params = request.get_json()
    send_configuration(client, params)
    return {"Result": "Configuration successfully sent"}, 201


def mqtt_connect():
    client.username_pw_set(
        username=os.getenv("MQTT_USERNAME", "demo_user"),
        password=os.getenv("MQTT_PASSWORD", "change_me_server_password"),
    )
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(os.getenv("MQTT_SERVER_ADDRESS"), int(os.getenv("MQTT_SERVER_PORT")), 60)
    client.loop_start()


if __name__ == "__main__":
    mqtt_connect()
    app.run(host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", "5000")), use_reloader=False)
