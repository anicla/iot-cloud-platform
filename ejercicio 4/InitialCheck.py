import RPi.GPIO as GPIO
from pn532.spi import PN532_SPI


def main():
    pn532 = PN532_SPI(debug=False, reset=20, cs=4)
    ic, ver, rev, support = pn532.get_firmware_version()
    print(f"Found PN532 with firmware version: {ver}.{rev}")
    pn532.SAM_configuration()
    print("Waiting for RFID/NFC card...")
    while True:
        uid = pn532.read_passive_target(timeout=0.5)
        print(".", end="", flush=True)
        if uid is None:
            continue
        print("\nFound card with UID:", [hex(i) for i in uid])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()

