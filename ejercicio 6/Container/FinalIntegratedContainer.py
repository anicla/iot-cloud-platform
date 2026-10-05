import signal
import threading
import time

import RPi.GPIO as GPIO


BUTTON_PIN = 16
motor_enabled = True
temperature = 26.0
door_open = False
motor_status = "Off"
lock = threading.Lock()


def button_callback(channel):
    global motor_enabled
    with lock:
        motor_enabled = not motor_enabled
        print(f"DC Motor habilitado: {motor_enabled}")


def motor_manager():
    global motor_status
    while True:
        with lock:
            if motor_enabled and not door_open and temperature > 25:
                motor_status = "On"
                speed = min(100, 80 + int((temperature - 25) * 2))
            else:
                motor_status = "Off"
                speed = 0
        print(f"Motor {motor_status}, velocidad {speed}")
        time.sleep(1)


def lcd_manager():
    while True:
        with lock:
            print(f"LCD -> Temp:{temperature:.1f} Door:{door_open} DC Motor:{motor_status}")
        time.sleep(2)


def cleanup(signum=None, frame=None):
    GPIO.cleanup()
    raise SystemExit


def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=150)
    signal.signal(signal.SIGINT, cleanup)

    threading.Thread(target=motor_manager, daemon=True).start()
    threading.Thread(target=lcd_manager, daemon=True).start()
    signal.pause()


if __name__ == "__main__":
    main()

