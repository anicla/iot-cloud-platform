# Ejercicio 9 - Microservicios IoT

Amplia la solucion MQTT con microservicios Flask y bases MariaDB independientes para dispositivos y telemetria.

## Componentes

- Mosquitto: broker MQTT con usuarios generados en arranque.
- Message router: puente entre MQTT y los microservicios HTTP.
- Devices microservice: sesiones y configuracion de contenedores.
- Telemetry microservice: almacenamiento y consulta de medidas.

## Ejecutar

```bash
cd IoTCloudServices
cp .env.example .env
docker compose -p iot-services up --build
```

Los puertos expuestos son `1883` para MQTT, `5000` para el router, `5001` para telemetria y `5002` para dispositivos.
