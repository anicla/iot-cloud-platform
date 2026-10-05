from datetime import datetime
from time import sleep

from Adafruit_LCD1602 import Adafruit_CharLCD
from PCF8574 import PCF8574_GPIO


PCF8574_ADDRESS = 0x27
PCF8574A_ADDRESS = 0x3F


def get_time_now():
    return datetime.now().strftime("%H:%M:%S")


def setup_lcd():
    try:
        mcp = PCF8574_GPIO(PCF8574_ADDRESS)
    except Exception:
        try:
            mcp = PCF8574_GPIO(PCF8574A_ADDRESS)
        except Exception:
            print("I2C Address Error!")
            raise

    lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4, 5, 6, 7], GPIO=mcp)
    mcp.output(3, 1)
    lcd.begin(16, 2)
    lcd.clear()
    return lcd


def destroy(lcd):
    lcd.clear()


def main():
    lcd = setup_lcd()
    try:
        while True:
            lcd.clear()
            lcd.setCursor(0, 0)
            lcd.message("Prueba Inicial\n")
            lcd.message(get_time_now())
            sleep(1)
    finally:
        destroy(lcd)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

