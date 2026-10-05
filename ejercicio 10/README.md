# Ejercicio 10 - Visualizacion de datos IoT

Frontend estatico y backend Flask para consultar los microservicios del ejercicio 9 y visualizar contenedores, telemetria y configuracion.

## Ejecutar

Arranca primero `ejercicio 9/IoTCloudServices`. Despues:

```bash
cd IoTCloudServices
cp .env.example .env
# Configura GOOGLE_MAPS_API_KEY en .env.
docker compose -p iot-web up --build
```

La web queda disponible en `http://localhost/` y el backend en `http://localhost:5003/`.

Para la vista de mapa, configura una clave propia restringida al dominio de pruebas en `.env`. Se carga al arrancar el frontend y es visible en el navegador.

La fase 9 crea la red compartida `iot_platform`. Usa `-p iot-services` para ese despliegue y `-p iot-web` para este, evitando colisiones entre carpetas llamadas `IoTCloudServices`.
