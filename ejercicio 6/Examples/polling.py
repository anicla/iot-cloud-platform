import time

import RPi.GPIO as GPIO


BUTTON_PIN = 16


GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pressed = False

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW and not pressed:
            print("Boton pulsado")
            pressed = True
        elif GPIO.input(BUTTON_PIN) == GPIO.HIGH and pressed:
            print("Boton liberado")
            pressed = False
        time.sleep(0.02)
except KeyboardInterrupt:
    GPIO.cleanup()

