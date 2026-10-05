import re

import RPi.GPIO as GPIO
from cryptography.fernet import Fernet
from pn532 import pn532 as nfc
from pn532.spi import PN532_SPI


KEY_FILE = "fernet.key"


def get_reader_uid():
    pn532 = PN532_SPI(debug=False, reset=20, cs=4)
    pn532.SAM_configuration()
    return pn532


def wait_for_uid(pn532):
    uid = None
    while uid is None:
        uid = pn532.read_passive_target(timeout=0.5)
    return uid


def read_block(pn532, uid, block):
    key_a = b"\xFF\xFF\xFF\xFF\xFF\xFF"
    pn532.mifare_classic_authenticate_block(
        uid, block_number=block, key_number=nfc.MIFARE_CMD_AUTH_A, key=key_a
    )
    return pn532.mifare_classic_read_block(block)


def parse_index(raw):
    text = raw.decode("utf-8").strip()
    match = re.search(r"B-(\d+);Size-(\d+)", text)
    return int(match.group(1)), int(match.group(2))


def read_payload(pn532, uid, index_block):
    start_block, size = parse_index(read_block(pn532, uid, index_block))
    blocks_needed = (size + 15) // 16
    payload = b""
    for block in range(start_block, start_block + blocks_needed):
        payload += read_block(pn532, uid, block)
    return payload[:size]


def decrypt_payload(payload):
    with open(KEY_FILE, "rb") as file_key:
        fernet = Fernet(file_key.read())
    return fernet.decrypt(payload).decode("utf-8")


def read_info_from_card(pn532):
    uid = wait_for_uid(pn532)
    my_date = decrypt_payload(read_payload(pn532, uid, 4))
    my_id = decrypt_payload(read_payload(pn532, uid, 6))
    return my_date.replace("Date:", ""), my_id.replace("ID:", "")


if __name__ == "__main__":
    try:
        reader = get_reader_uid()
        print(read_info_from_card(reader))
    finally:
        GPIO.cleanup()

