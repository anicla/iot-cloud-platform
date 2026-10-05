import datetime
import json
import os
import random
import socket
import threading
import time

import paho.mqtt.client as mqtt


container_id = "UC3M-Container-" + str(random.randint(1, 5))
hostname = socket.gethostname()
connection_granted = False
sampling_frequency = 10
disconnected = False
client = mqtt.Client()


def now_ms():
    return datetime.datetime.timestamp(datetime.datetime.now()) * 1000


def build_telemetry():
    temperature = random.uniform(0, 35)
    return {
        "Container_id": container_id,
        "Position": {"Latitude": 40.33 + random.random() / 100, "Longitude": -3.76 - random.random() / 100},
        "Temperature": temperature,
        "Humidity": random.uniform(30, 90),
        "Door Open": random.choice([True, False]),
        "Driver": "Driver 1",
        "Refrigerator Fan": 0 if temperature <= 25 else min(100, 80 + int((temperature - 25) * 2)),
        "time_stamp": datetime.datetime.now().isoformat(),
    }


def on_connect(mqtt_client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    request_topic = f"/fic/containers/{hostname}/request_access/"
    config_topic = f"/fic/containers/{hostname}/config/"
    mqtt_client.subscribe(config_topic)
    mqtt_client.publish(request_topic, json.dumps({"Container_id": container_id, "Timestamp": now_ms()}), qos=1)


def on_message(mqtt_client, userdata, msg):
    global connection_granted, sampling_frequency, disconnected
    print(f"Config received: {msg.payload.decode()}")
    data = json.loads(msg.payload.decode())
    if data.get("Authorization") == "True":
        connection_granted = True
    elif data.get("Authorization") == "False":
        disconnected = True
    if "Sampling_Frequency" in data:
        sampling_frequency = float(data["Sampling_Frequency"])


def mqtt_communications():
    client.username_pw_set(
        username=os.getenv("MQTT_USERNAME", "demo_device"),
        password=os.getenv("MQTT_PASSWORD", "change_me_device_password"),
    )
    client.on_connect = on_connect
    client.on_message = on_message
    session_topic = f"/fic/containers/{hostname}/session/"
    client.will_set(session_topic, json.dumps({"Container_id": container_id, "Status": "Off - Unregulate Disconnection"}))
    client.connect(os.getenv("MQTT_SERVER_ADDRESS", "localhost"), int(os.getenv("MQTT_SERVER_PORT", "1883")), 60)
    client.loop_start()
    telemetry_topic = f"/fic/containers/{hostname}/telemetry/"
    while not disconnected:
        if connection_granted:
            client.publish(telemetry_topic, json.dumps(build_telemetry()), qos=1)
            time.sleep(sampling_frequency)
        else:
            time.sleep(2)


if __name__ == "__main__":
    mqtt_communications()
