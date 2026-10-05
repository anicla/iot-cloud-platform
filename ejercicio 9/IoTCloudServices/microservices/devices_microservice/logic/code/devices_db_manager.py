import os

import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DBHOST"),
        user=os.getenv("DBUSER"),
        password=os.getenv("DBPASSWORD"),
        database=os.getenv("DBDATABASE"),
    )


def retrieve_containers():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT container_id, container_hostname, active, telemetry_rate, sensors_rate FROM containers")
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result


def retrieve_active_containers():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT container_id, container_hostname, telemetry_rate, sensors_rate FROM containers WHERE active = 1")
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result


def register_container_connection(data):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE containers SET active = 1, container_hostname = %s WHERE container_id = %s",
        (data["container_hostname"], data["container_id"]),
    )
    connection.commit()
    updated = cursor.rowcount
    cursor.close()
    connection.close()
    if updated:
        return {"container_id": data["container_id"], "active": "True", "Authorization": "True"}
    return {}


def register_container_disconnection(data):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE containers SET active = 0, container_hostname = '' WHERE container_id = %s",
        (data["container_id"],),
    )
    connection.commit()
    updated = cursor.rowcount
    cursor.close()
    connection.close()
    if updated:
        return {"container_id": data["container_id"], "active": "False"}
    return {}


def retrieve_container(params):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT container_id, container_hostname, telemetry_rate, sensors_rate, active AS status FROM containers WHERE container_id = %s",
        (params["container_id"],),
    )
    result = cursor.fetchone() or {}
    cursor.close()
    connection.close()
    return result


def save_container_config(data):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT active, container_hostname FROM containers WHERE container_id = %s", (data["container_id"],))
    current = cursor.fetchone()
    if not current or current["active"] != 1:
        cursor.close()
        connection.close()
        return {}

    telemetry_rate = data.get("telemetry_rate", data.get("rate", 10))
    sensors_rate = data.get("sensors_rate", data.get("sampling", 10))
    cursor.execute(
        "UPDATE containers SET telemetry_rate = %s, sensors_rate = %s WHERE container_id = %s",
        (telemetry_rate, sensors_rate, data["container_id"]),
    )
    connection.commit()
    result = {
        "container_id": data["container_id"],
        "container_hostname": current["container_hostname"],
        "telemetry_rate": float(telemetry_rate),
        "sensors_rate": float(sensors_rate),
        "Sampling_Frequency": float(sensors_rate),
    }
    cursor.close()
    connection.close()
    return result
