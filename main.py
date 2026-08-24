import qrcode


def build_wifi_payload(ssid: str, password: str, enc_type: str) -> str:
    return f"WIFI:S:{ssid};T:{enc_type.upper()};P:{password};;"


def main():
    print("Hello from qr!")
    # 1. Datos a codificar
    datos = "WIFI:S:xeviestudi;T:WPA;P:xestud12345;;"

    # 2. Generar código QR
    img = qrcode.make(datos)

    # 3. Guardar la imagen
    img.save("codigo_qr.png")
    print("Código QR generado exitosamente.")


if __name__ == "__main__":
    main()
