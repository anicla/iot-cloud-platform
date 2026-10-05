import datetime
import math
import random
import string

import RPi.GPIO as GPIO
from cryptography.fernet import Fernet
from pn532 import pn532 as nfc
from pn532.spi import PN532_SPI


KEY_FILE = "fernet.key"
INDEX_DATE_BLOCK = 4
INDEX_ID_BLOCK = 6
DATE_DATA_BLOCK = 8
ID_DATA_BLOCK = 12


def load_fernet():
    with open(KEY_FILE, "rb") as file_key:
        return Fernet(file_key.read())


def chunks_16(data):
    padded = data + b" " * ((16 - len(data) % 16) % 16)
    return [padded[i:i + 16] for i in range(0, len(padded), 16)]


def store_block(pn532, uid, data, block):
    key_a = b"\xFF\xFF\xFF\xFF\xFF\xFF"
    pn532.mifare_classic_authenticate_block(
        uid, block_number=block, key_number=nfc.MIFARE_CMD_AUTH_A, key=key_a
    )
    pn532.mifare_classic_write_block(block, data)
    if pn532.mifare_classic_read_block(block) == data:
        print(f"write block {block} successfully")


def store_bytes(pn532, uid, payload, start_block):
    blocks = chunks_16(payload)
    for index, block_data in enumerate(blocks):
        store_block(pn532, uid, block_data, start_block + index)
    return len(payload)


def random_driver_id():
    return "".join(random.choice(string.digits) for _ in range(8)) + random.choice(string.ascii_uppercase)


def main():
    pn532 = PN532_SPI(debug=False, reset=20, cs=4)
    pn532.SAM_configuration()
    print("Acerca una tarjeta NFC...")
    uid = None
    while uid is None:
        uid = pn532.read_passive_target(timeout=0.5)

    fernet = load_fernet()
    valid_until = (datetime.date.today() + datetime.timedelta(days=30)).strftime("%d-%m-%Y")
    date_payload = fernet.encrypt(f"Date:{valid_until}".encode("utf-8"))
    id_payload = fernet.encrypt(f"ID:{random_driver_id()}".encode("utf-8"))

    date_size = store_bytes(pn532, uid, date_payload, DATE_DATA_BLOCK)
    id_size = store_bytes(pn532, uid, id_payload, ID_DATA_BLOCK)

    date_index = f"DT:B-{DATE_DATA_BLOCK:02d};Size-{date_size:03d}".encode("utf-8")
    id_index = f"ID:B-{ID_DATA_BLOCK:02d};Size-{id_size:03d}".encode("utf-8")
    store_block(pn532, uid, date_index[:16].ljust(16, b" "), INDEX_DATE_BLOCK)
    store_block(pn532, uid, id_index[:16].ljust(16, b" "), INDEX_ID_BLOCK)
    print("Tarjeta escrita")


if __name__ == "__main__":
    try:
        main()
    finally:
        GPIO.cleanup()

