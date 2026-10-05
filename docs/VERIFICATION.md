# Verificacion local

Comprobaciones realizadas el 2026-10-05 en Linux con Docker Engine 24 y Docker Compose 1.29.2:

- Sintaxis de los 27 archivos Python analizada sin generar caches.
- Sintaxis de entrypoints comprobada con `sh -n`.
- Todos los archivos Compose validados con `docker-compose config -q`.
- Construidas las imagenes de servicios de la fase 9, web de la fase 10 y simulador de la fase 8.
- Arrancados Mosquitto, las dos bases MariaDB, los microservicios, el router y la web en una red compartida.
- Registro de un contenedor simulado confirmado en el servicio de dispositivos.
- Consulta de posiciones y telemetria a traves del backend web: HTTP 200 con datos.
- Cambio de configuracion desde la API web: HTTP 200; recepcion de `Sampling_Frequency` confirmada en el simulador.
- Frontend y `runtime-config.js` servidos por Apache correctamente.
- Revision de patrones habituales de secretos en el estado actual: sin contrasenas academicas originales, claves privadas, claves Maps reales ni credenciales de cuentas de servicio identificadas.

Las pruebas usan contrasenas publicas de demostracion y recursos temporales. No verifican hardware Raspberry Pi, despliegue GCP, rendimiento, seguridad de produccion ni la representacion visual del mapa con una clave Google Maps real. Tampoco certifican la ausencia de secretos en todo el historial.
