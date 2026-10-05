from time import sleep

import RPi.GPIO as GPIO
import adafruit_dht
import board
from Adafruit_LCD1602 import Adafruit_CharLCD
from PCF8574 import PCF8574_GPIO


class PantallaDHT11:
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.sensor = adafruit_dht.DHT11(board.D12)
        self.lcd = self._setup_lcd()

    def _setup_lcd(self):
        try:
            mcp = PCF8574_GPIO(0x27)
        except Exception:
            mcp = PCF8574_GPIO(0x3F)
        lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4, 5, 6, 7], GPIO=mcp)
        mcp.output(3, 1)
        lcd.begin(16, 2)
        lcd.clear()
        return lcd

    def read_sensor(self):
        return self.sensor.temperature, self.sensor.humidity

    def show_values(self, motor_status=None):
        temperature, humidity = self.read_sensor()
        self.lcd.clear()
        self.lcd.setCursor(0, 0)
        self.lcd.message(f"Temp:{temperature:.1f}C\n")
        suffix = f" M:{motor_status}" if motor_status else ""
        self.lcd.message(f"Hum:{humidity:.1f}%{suffix}")
        return temperature, humidity

    def ejecutar(self):
        while True:
            try:
                self.show_values()
            except RuntimeError as error:
                print(f"Lectura DHT11 no valida: {error}")
            sleep(1)

    def destroy(self):
        self.lcd.clear()


if __name__ == "__main__":
    pantalla = PantallaDHT11()
    try:
        pantalla.ejecutar()
    except KeyboardInterrupt:
        pantalla.destroy()
        GPIO.cleanup()

