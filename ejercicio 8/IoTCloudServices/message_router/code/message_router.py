import datetime
import json
import os
import random
import threading
import time

import paho.mqtt.client as mqtt


client = mqtt.Client()
connected_containers = []
authorised_containers = [f"UC3M-Container-{i}" for i in range(1, 6)]
telemetry_log = []


def find_authorised_container(container_id):
    return container_id in authorised_containers


def is_connected(container_id):
    for position, item in enumerate(connected_containers):
        if item["Container_id"] == container_id:
            return True, position
    return False, -1


def register_container_connection(container_id, container_hostname):
    connected_containers.append({"Container_id": container_id, "Container_hostname": container_hostname})


def on_connect(mqtt_client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    if rc == 0:
        topic = "/fic/containers/+/request_access/"
        mqtt_client.subscribe(topic)
        print("Subscribed to", topic)


def on_message(mqtt_client, userdata, msg):
    topic = msg.topic.split("/")
    print(f"Message on {msg.topic}: {msg.payload.decode()}")
    data = json.loads(msg.payload.decode())

    if "request_access" in msg.topic:
        hostname = topic[-3]
        allowed = find_authorised_container(data["Container_id"])
        already_connected, _ = is_connected(data["Container_id"])
        authorization = allowed and not already_connected
        if authorization:
            register_container_connection(data["Container_id"], hostname)
            mqtt_client.subscribe(f"/fic/containers/{hostname}/telemetry/")
        response = {
            "Container_id": data["Container_id"],
            "Authorization": str(authorization),
            "Timestamp": datetime.datetime.timestamp(datetime.datetime.now()) * 1000,
        }
        mqtt_client.publish(f"/fic/containers/{hostname}/config/", json.dumps(response), qos=1)

    if "telemetry" in msg.topic:
        telemetry_log.append(data)
        print("Telemetry stored locally:", data)


def configuration_sender():
    while True:
        for container in connected_containers:
            frequency = round(random.uniform(5, 15), 1)
            message = {
                "Container_id": container["Container_id"],
                "Sampling_Frequency": frequency,
                "Timestamp": datetime.datetime.timestamp(datetime.datetime.now()) * 1000,
            }
            topic = f"/fic/containers/{container['Container_hostname']}/config/"
            client.publish(topic, json.dumps(message), qos=1)
        time.sleep(60)


def main():
    client.username_pw_set(
        username=os.getenv("MQTT_USERNAME", "demo_user"),
        password=os.getenv("MQTT_PASSWORD", "change_me_server_password"),
    )
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(os.getenv("MQTT_SERVER_ADDRESS", "localhost"), int(os.getenv("MQTT_SERVER_PORT", "1883")), 60)
    threading.Thread(target=configuration_sender, daemon=True).start()
    client.loop_forever()


if __name__ == "__main__":
    main()
