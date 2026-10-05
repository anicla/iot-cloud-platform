import time

import RPi.GPIO as GPIO


SERVO_PIN = 21
servo_object = None


def setup_devices():
    global servo_object
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(SERVO_PIN, GPIO.OUT)
    servo_object = GPIO.PWM(SERVO_PIN, 50)
    servo_object.start(0)


def set_angle(angle, servo):
    duty = 2 + (angle / 18)
    servo.ChangeDutyCycle(duty)
    time.sleep(0.5)
    servo.ChangeDutyCycle(0)


if __name__ == "__main__":
    try:
        setup_devices()
        set_angle(0, servo_object)
        time.sleep(2)
        set_angle(90, servo_object)
        time.sleep(2)
        set_angle(0, servo_object)
    finally:
        GPIO.cleanup()

