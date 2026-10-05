#!/bin/sh
set -eu

: "${MQTT_SERVER_USERNAME:=demo_user}"
: "${MQTT_SERVER_PASSWORD:=change_me_server_password}"
: "${MQTT_DEVICE_USERNAME:=demo_device}"
: "${MQTT_DEVICE_PASSWORD:=change_me_device_password}"

mosquitto_passwd -b -c /etc/mosquitto/passwd "$MQTT_SERVER_USERNAME" "$MQTT_SERVER_PASSWORD"

if [ "$MQTT_DEVICE_USERNAME" != "$MQTT_SERVER_USERNAME" ]; then
  mosquitto_passwd -b /etc/mosquitto/passwd "$MQTT_DEVICE_USERNAME" "$MQTT_DEVICE_PASSWORD"
fi

exec /usr/sbin/mosquitto -c /etc/mosquitto/mosquitto.conf
