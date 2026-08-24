# Design: Wi-Fi QR CLI Arguments

Date: 2026-08-24
Status: approved

## Context

The project is a single-script Python tool (`main.py`) that generates a Wi-Fi
QR code image from hardcoded credentials (`WIFI:S:xeviestudi;T:WPA;P:...;;`)
using the `qrcode` and `pillow` libraries. It always writes `codigo_qr.png`.

## Goal

Let the user pass the SSID and password as command-line arguments, with
optional control over the encryption type and the output filename.

## CLI interface

```
python main.py --ssid <name> --password <pass> [--type wpa|wep|none] [-o codigo_qr.png]
```

| Flag | Required | Default | Notes |
|------|----------|---------|-------|
| `--ssid` | yes | — | Network name (S) |
| `--password` | conditional | — | Required when `--type` is `wpa` or `wep`; may be omitted for `none` |
| `--type` | no | `wpa` | Choices: `wpa`, `wep`, `none` (T) |
| `-o`, `--output` | no | `codigo_qr.png` | Output image path |

## Behavior

- The QR payload keeps the existing format exactly:
  `WIFI:S:{ssid};T:{TYPE};P:{password};;` where `{TYPE}` is the uppercased
  type (`WPA`, `WEP`, or `NONE`) and `{password}` is empty for `none`.
- A missing `--password` when the type requires one produces an argparse error
  (usage message, exit code 2); no file is written.
- On success the image is saved to the output path and a success message
  including that path is printed (Spanish, matching current messages).

## Architecture

Single file (`main.py`), stdlib only for argument handling (`argparse`):

- `build_wifi_payload(ssid, password, enc_type) -> str` — pure function that
  builds the `WIFI:...` payload string. No I/O, unit-testable in isolation.
- `main(argv=None)` — parses arguments, validates the password requirement,
  generates the QR with `qrcode.make`, saves it, prints the success message.

No new dependencies. No module split (script stays under ~50 lines).

## Error handling

- Unknown flags, missing `--ssid`, invalid `--type` value: handled by
  argparse (usage message, exit code 2).
- Missing `--password` for `wpa`/`wep`: raised as an argparse error from
  `main()` after parsing (`parser.error(...)`), exit code 2, no file written.

## Testing

`unittest`-based tests (stdlib) asserting `build_wifi_payload` output:

1. `wpa` with a password → exact expected payload string.
2. `wep` with a password → exact expected payload string.
3. `none` without a password → exact expected payload string (`P:;`).

## Out of scope

- Interactive/password-prompt input.
- New dependencies (e.g., `click`, `typer`).
- Module/file splitting.
- Logo, color, or QR sizing options.
