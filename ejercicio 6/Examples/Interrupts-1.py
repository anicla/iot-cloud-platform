import RPi.GPIO as GPIO


BUTTON_PIN = 16


GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        GPIO.wait_for_edge(BUTTON_PIN, GPIO.FALLING)
        print("Boton pulsado")
        GPIO.wait_for_edge(BUTTON_PIN, GPIO.RISING)
        print("Boton liberado")
except KeyboardInterrupt:
    GPIO.cleanup()

