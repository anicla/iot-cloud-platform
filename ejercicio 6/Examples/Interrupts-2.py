import signal

import RPi.GPIO as GPIO


BUTTON_PIN = 16


def button_pressed_callback(channel):
    print(f"Boton pulsado en GPIO {channel}")


def cleanup(signum, frame):
    GPIO.cleanup()
    raise SystemExit


GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_pressed_callback, bouncetime=100)
signal.signal(signal.SIGINT, cleanup)
signal.pause()

