# Ejercicio 1 - Instalacion y configuracion

Este ejercicio no pide un programa principal, sino preparar la Raspberry Pi.

## Checklist de entrega

1. Crear imagen con Raspberry Pi Imager.
2. Configurar usuario, password, hostname, zona horaria, teclado y SSH.
3. Arrancar la Raspberry Pi.
4. Ejecutar `sudo raspi-config` y expandir el sistema de ficheros.
5. Comprobar red:

```bash
hostname -I
ping -c 4 google.com
```

6. Comprobar acceso remoto:

```bash
ssh usuario@raspberrypi.local
```

7. Instalar paquetes base:

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y git python3-pip python3-venv
```

8. Habilitar interfaces que se usaran en practicas posteriores:

```bash
sudo raspi-config
# Interface Options -> I2C -> Enable
# Interface Options -> SPI -> Enable
# Interface Options -> SSH -> Enable
```

## Comandos utiles para localizar la Raspberry

```bash
arp -a | grep raspberry
sudo nmap -sP 192.168.1.0/24 | grep raspberry
```

