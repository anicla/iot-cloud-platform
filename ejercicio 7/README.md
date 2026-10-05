# Ejercicio 7 - Contenedores y gemelo digital

Simula una unidad de control que recibe datos de sensores por sockets TCP y un contenedor que genera posicion, ambiente, puerta y refrigeracion.

## Ejecutar

```bash
docker compose up --build
```

La unidad de control escucha en `localhost:9000`. El simulador envia mensajes periodicos usando `UC_SIMULATOR_HOST`, `UC_SIMULATOR_PORT` y `SAMPLING_FREQUENCY`.
