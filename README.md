# Wi-Fi QR CODE GENERATOR

Generates a QR code image for sharing a Wi-Fi network. Scan it with your phone camera to connect.

## Usage

```bash
uv run python main.py --ssid <net_name> --password <net_password> [--type wpa|wep|none] [-o qr_file.png]
```

| Flag           | Description                                                 |
| -------------- | ----------------------------------------------------------- |
| `--ssid`       | Network name (required)                                     |
| `--password`   | Network password (required when `--type` is `wpa` or `wep`) |
| `--type`       | Encryption type: `wpa` (default), `wep`, or `none`          |
| `-o, --output` | Output image path (default: `codigo_qr.png`)                |

## Example

```bash
uv run python main.py --ssid my_wifi --password my_wifi_12345
```

Prints `Código QR generado exitosamente en codigo_qr.png.` when done.

## Tests

```bash
uv run python -m unittest -v
```
