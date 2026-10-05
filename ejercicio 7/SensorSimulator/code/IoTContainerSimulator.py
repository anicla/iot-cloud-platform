import datetime
import json
import os
import random
import socket
import string
import threading
import time


UC_SIMULATOR_HOST = os.getenv("UC_SIMULATOR_HOST", "control_unit")
UC_SIMULATOR_PORT = int(os.getenv("UC_SIMULATOR_PORT", "9000"))
sampling_frequency = float(os.getenv("SAMPLING_FREQUENCY", "10"))
temperature = random.uniform(0, 30)
humidity = random.uniform(30, 90)
door_id = "".join(random.choice(string.digits) for _ in range(8)) + random.choice(string.ascii_uppercase)


def now():
    return datetime.datetime.now().isoformat()


def send_message(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((UC_SIMULATOR_HOST, UC_SIMULATOR_PORT))
        client.sendall(json.dumps(message).encode("utf-8"))
        client.recv(1024)


def simulate_positions():
    lat, lon = 40.33256, -3.76516
    while True:
        lat += random.uniform(-0.001, 0.001)
        lon += random.uniform(-0.001, 0.001)
        send_message({"Type": "GNSS", "Position": {"Latitude": lat, "Longitude": lon}, "Timestamp": now()})
        time.sleep(sampling_frequency)


def simulate_environment():
    global temperature, humidity
    while True:
        temperature += random.uniform(-0.05, 0.05) * max(temperature, 1)
        humidity += random.uniform(-0.05, 0.05) * max(humidity, 1)
        temperature = max(-5, min(40, temperature))
        humidity = max(0, min(100, humidity))
        send_message({"Type": "Environment", "Temperature": temperature, "Humidity": humidity, "Timestamp": now()})
        time.sleep(sampling_frequency)


def simulate_door():
    while True:
        status = random.choice(["Close", "Close", "Open"])
        send_message({"Type": "Door", "Status": status, "ID": door_id if status == "Open" else "", "Timestamp": now()})
        time.sleep(sampling_frequency)


def simulate_refrigerator():
    while True:
        speed = 0
        status = "Off"
        if temperature > 25:
            status = "On"
            speed = min(100, 80 + int((temperature - 25) * 2))
        send_message({"Type": "Refrigerator", "Status": status, "Velocidad": speed, "Timestamp": now()})
        time.sleep(sampling_frequency)


def main():
    threads = [
        threading.Thread(target=simulate_positions, daemon=True),
        threading.Thread(target=simulate_environment, daemon=True),
        threading.Thread(target=simulate_door, daemon=True),
        threading.Thread(target=simulate_refrigerator, daemon=True),
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()

