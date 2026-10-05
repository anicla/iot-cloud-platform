import os

import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DBHOST"),
        user=os.getenv("DBUSER"),
        password=os.getenv("DBPASSWORD"),
        database=os.getenv("DBDATABASE"),
    )


def register_new_telemetry(data):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        sql = """
            INSERT INTO telemetry
            (container_id, latitude, longitude, temperature, humidity, door_open, current_driver_id, refrigerator_fan, time_stamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            data["Container_id"],
            data["Position"]["Latitude"],
            data["Position"]["Longitude"],
            data["Temperature"],
            data["Humidity"],
            int(bool(data["Door Open"])),
            data["Driver"],
            data["Refrigerator Fan"],
            data["time_stamp"],
        )
        cursor.execute(sql, values)
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as error:
        print(error)
        return False


def query_telemetry(params):
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        sql = """
            SELECT container_id, latitude, longitude, temperature, humidity, door_open,
                   current_driver_id, refrigerator_fan, time_stamp
            FROM telemetry
            WHERE container_id = %s
            ORDER BY id DESC
            LIMIT 100
        """
        cursor.execute(sql, (params["container_id"],))
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result
    except Exception as error:
        print(error)
        return []


def retrieve_containers_last_position():
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        sql = """
            SELECT t.container_id AS Container_id, t.latitude AS Latitude, t.longitude AS Longitude
            FROM telemetry t
            INNER JOIN (
                SELECT container_id, MAX(id) AS max_id
                FROM telemetry
                GROUP BY container_id
            ) last_t ON t.container_id = last_t.container_id AND t.id = last_t.max_id
        """
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return "", result
    except Exception as error:
        return str(error), []

