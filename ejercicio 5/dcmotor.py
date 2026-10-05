import time

import RPi.GPIO as GPIO


class ControlMotorDC:
    def __init__(self, pin_a=5, pin_b=6, pin_e=13):
        self.pin_a = pin_a
        self.pin_b = pin_b
        self.pin_e = pin_e
        self.dc_motor_object = None
        self.setup_devices()

    def setup_devices(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin_a, GPIO.OUT)
        GPIO.setup(self.pin_b, GPIO.OUT)
        GPIO.setup(self.pin_e, GPIO.OUT)
        GPIO.output(self.pin_a, True)
        GPIO.output(self.pin_b, False)
        self.dc_motor_object = GPIO.PWM(self.pin_e, 100)
        self.dc_motor_object.start(0)

    def cambiar_velocidad(self, requested_speed):
        requested_speed = max(0, min(100, int(requested_speed)))
        print(f"Cambiando la velocidad del motor a {requested_speed}")
        self.dc_motor_object.ChangeDutyCycle(requested_speed)

    def stop(self):
        self.cambiar_velocidad(0)


if __name__ == "__main__":
    motor = ControlMotorDC()
    speed = 80
    try:
        while True:
            motor.cambiar_velocidad(speed)
            time.sleep(5)
            if speed < 100:
                speed += 5
    except KeyboardInterrupt:
        print("Limpiando configuracion de GPIO...")
        GPIO.cleanup()

