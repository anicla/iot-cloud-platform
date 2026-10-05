# Ejercicio 8 - MQTT y Mosquitto

Arquitectura basica con broker MQTT, router de mensajes y simulador de contenedor refrigerado.

## Servicios

- `IoTCloudServices`: broker Mosquitto y router de mensajes.
- `IoTContainer`: simulador que solicita acceso, recibe configuracion y publica telemetria.

## Ejecutar

```bash
cd IoTCloudServices
cp .env.example .env
docker compose up --build
```

En otra terminal o maquina:

```bash
cd IoTContainer
cp .env.example .env
docker compose up --build
```

Edita `IoTContainer/.env` para que `MQTT_SERVER_ADDRESS` apunte al host donde corre Mosquitto.
