from cryptography.fernet import Fernet


KEY_FILE = "fernet.key"


def generate_key(file_name=KEY_FILE):
    key = Fernet.generate_key()
    with open(file_name, "wb") as file_key:
        file_key.write(key)
    print(f"Clave guardada en {file_name}")
    return key


if __name__ == "__main__":
    generate_key()

