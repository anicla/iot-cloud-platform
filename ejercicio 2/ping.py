import os


def main():
    host = "8.8.8.8"
    response = os.system(f"ping -c 4 {host}")
    if response == 0:
        print(f"{host} responde correctamente")
    else:
        print(f"No se ha podido contactar con {host}")


if __name__ == "__main__":
    main()

