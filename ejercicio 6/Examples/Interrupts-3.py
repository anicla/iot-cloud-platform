import signal

import RPi.GPIO as GPIO


BUTTON_PIN = 16


def button_changed_callback(channel):
    if GPIO.input(channel) == GPIO.LOW:
        print("Boton pulsado")
    else:
        print("Boton liberado")


def cleanup(signum, frame):
    GPIO.cleanup()
    raise SystemExit


GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(BUTTON_PIN, GPIO.BOTH, callback=button_changed_callback, bouncetime=50)
signal.signal(signal.SIGINT, cleanup)
signal.pause()

