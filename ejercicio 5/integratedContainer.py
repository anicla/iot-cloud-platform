import random
import threading
import time

import RPi.GPIO as GPIO
from dcmotor import ControlMotorDC


temperature = 20.0
humidity = 50.0
door_open = False
last_authorized_id = ""
motor_enabled = True
motor_status = "Off"
lock = threading.Lock()


def screen_and_dht_manager():
    global temperature, humidity
    while True:
        with lock:
            temperature += random.uniform(-0.5, 0.8)
            humidity += random.uniform(-1, 1)
            print(f"LCD -> T:{temperature:.1f} H:{humidity:.1f} Motor:{motor_status} ID:{last_authorized_id}")
        time.sleep(1)


def nfc_and_servo_manager():
    global door_open, last_authorized_id
    valid_ids = ["12345678A", "87654321B"]
    while True:
        authorized = random.choice([False, False, True])
        with lock:
            if authorized:
                door_open = True
                last_authorized_id = random.choice(valid_ids)
                print(f"Acceso autorizado: {last_authorized_id}")
            else:
                door_open = False
        time.sleep(5)
        with lock:
            door_open = False


def dc_motor_manager():
    global motor_status
    motor = ControlMotorDC(pin_a=5, pin_b=6, pin_e=13)
    while True:
        with lock:
            temp = temperature
            opened = door_open
            enabled = motor_enabled

        if enabled and not opened and temp > 25:
            speed = min(100, 80 + int((temp - 25) * 2))
            motor_status = "On"
        else:
            speed = 0
            motor_status = "Off"

        motor.cambiar_velocidad(speed)
        time.sleep(1)


def run_container():
    threads = [
        threading.Thread(target=screen_and_dht_manager, daemon=True),
        threading.Thread(target=nfc_and_servo_manager, daemon=True),
        threading.Thread(target=dc_motor_manager, daemon=True),
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    try:
        run_container()
    except KeyboardInterrupt:
        GPIO.cleanup()

