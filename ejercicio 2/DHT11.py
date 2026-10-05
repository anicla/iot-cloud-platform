import time

import RPi.GPIO as GPIO
import adafruit_dht
import board


READ_PERIOD_SECONDS = 2


class DHT11Reader:
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.sensor = adafruit_dht.DHT11(board.D12)

    def read(self):
        temperature_c = self.sensor.temperature
        humidity = self.sensor.humidity
        return temperature_c, humidity


def main():
    reader = DHT11Reader()
    while True:
        try:
            temperature_c, humidity = reader.read()
            print(f"Temp: {temperature_c:.1f} C, Humidity: {humidity:.1f}%")
        except RuntimeError as error:
            print(f"Lectura no valida: {error}")
        time.sleep(READ_PERIOD_SECONDS)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Limpiando configuracion de GPIO...")
        GPIO.cleanup()

