import argparse

import qrcode


def _escape(value: str) -> str:
    return (
        value.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace(":", "\\:")
    )


def build_wifi_payload(ssid: str, password: str, enc_type: str) -> str:
    return f"WIFI:S:{_escape(ssid)};T:{enc_type.upper()};P:{_escape(password)};;"


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Genera un código QR de red Wi-Fi.")
    parser.add_argument("--ssid", required=True, help="Nombre de la red (SSID)")
    parser.add_argument("--password", help="Contraseña de la red")
    parser.add_argument(
        "--type",
        dest="enc_type",
        choices=("wpa", "wep", "none"),
        default="wpa",
        help="Tipo de cifrado (predeterminado: wpa)",
    )
    parser.add_argument(
        "-o", "--output", default="codigo_qr.png", help="Ruta de la imagen a generar"
    )
    args = parser.parse_args(argv)

    if args.enc_type in ("wpa", "wep") and not args.password:
        parser.error(f"--password es obligatorio cuando --type es {args.enc_type}")

    payload = build_wifi_payload(args.ssid, args.password or "", args.enc_type)
    img = qrcode.make(payload)
    img.save(args.output)
    print(f"Código QR generado exitosamente en {args.output}.")


if __name__ == "__main__":
    main()
