import datetime
import json
import os
import socket
import threading


HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "9000"))

current_state = {
    "Position": {"Latitude": 0.0, "Longitude": 0.0},
    "Environment": {"Temperature": 0.0, "Humidity": 0.0},
    "Door": {"Status": "Close", "ID": ""},
    "Refrigerator": {"Status": "Off", "Velocidad": 0.0},
    "Timestamp": "",
}
lock = threading.Lock()


def process_received_message(message):
    global current_state
    data = json.loads(message)
    with lock:
        if data["Type"] == "GNSS":
            current_state["Position"] = data["Position"]
        elif data["Type"] == "Environment":
            current_state["Environment"] = {
                "Temperature": data["Temperature"],
                "Humidity": data["Humidity"],
            }
        elif data["Type"] == "Door":
            current_state["Door"] = {"Status": data["Status"], "ID": data["ID"]}
        elif data["Type"] == "Refrigerator":
            current_state["Refrigerator"] = {
                "Status": data["Status"],
                "Velocidad": data["Velocidad"],
            }
        current_state["Timestamp"] = data["Timestamp"]
        print(json.dumps(current_state, indent=2))


def client_listener(connection, address):
    print(f"{datetime.datetime.now()} - New connection {address}")
    with connection:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            process_received_message(data.decode("utf-8"))
            connection.sendall(b"ok")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(4)
        print(f"Unidad de Control escuchando en {HOST}:{PORT}")
        while True:
            connection, address = server.accept()
            threading.Thread(target=client_listener, args=(connection, address), daemon=True).start()


if __name__ == "__main__":
    main()

