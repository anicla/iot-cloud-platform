import datetime
import time

import RPi.GPIO as GPIO
from ReadNFCData import get_reader_uid, read_info_from_card
import Servomotor


VALID_IDS = {"12345678A", "87654321B"}


def is_valid(date_text, driver_id):
    valid_until = datetime.datetime.strptime(date_text, "%d-%m-%Y").date()
    return valid_until >= datetime.date.today() and driver_id in VALID_IDS


def main():
    Servomotor.setup_devices()
    pn532 = get_reader_uid()
    while True:
        card_date, driver_id = read_info_from_card(pn532)
        print(f"La fecha de caducidad de la tarjeta es: {card_date}")
        print(f"El id de la tarjeta es: {driver_id}")
        if is_valid(card_date, driver_id):
            Servomotor.set_angle(90, Servomotor.servo_object)
            time.sleep(5)
        Servomotor.set_angle(0, Servomotor.servo_object)
        time.sleep(5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
