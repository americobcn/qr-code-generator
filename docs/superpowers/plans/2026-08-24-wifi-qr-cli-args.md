# Wi-Fi QR CLI Arguments Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the hardcoded Wi-Fi credentials in `main.py` with command-line arguments (`--ssid`, `--password`, `--type`, `-o/--output`).

**Architecture:** Single-file script (`main.py`) using stdlib `argparse`. A pure function `build_wifi_payload()` builds the `WIFI:...` payload string; `main(argv)` parses arguments, validates them, generates the QR with `qrcode`, and saves it.

**Tech Stack:** Python >=3.12, `uv` for running, existing deps only (`qrcode`, `pillow`), stdlib `unittest` for tests.

## Global Constraints

- No new dependencies: only `argparse`, `unittest`, and existing `qrcode`/`pillow`.
- Payload format is exact: `WIFI:S:{ssid};T:{TYPE};P:{password};;` with `TYPE` uppercased (`WPA`/`WEP`/`NONE`).
- No SSID, password, or payload string may remain hardcoded in `main.py` source.
- User-facing messages (help text, errors, success) are in Spanish, matching current style.
- Argument errors exit with code 2 (argparse behavior) and write no file.
- Default output filename: `codigo_qr.png`.

## File Structure

- Modify: `main.py` — CLI entry point + `build_wifi_payload()` (whole file shown in Task 2).
- Create: `tests/test_main.py` — stdlib `unittest` tests for payload builder and CLI.

---

### Task 1: `build_wifi_payload()` (TDD)

**Files:**
- Create: `tests/test_main.py`
- Modify: `main.py` (add function only; `main()` untouched in this task)

**Interfaces:**
- Consumes: nothing.
- Produces: `build_wifi_payload(ssid: str, password: str, enc_type: str) -> str` in `main.py`, returning the exact `WIFI:...` payload.

- [ ] **Step 1: Write the failing test**

Create `tests/test_main.py`:

```python
import unittest

from main import build_wifi_payload


class BuildWifiPayloadTestCase(unittest.TestCase):
    def test_wpa_payload_matches_legacy_format(self):
        self.assertEqual(
            build_wifi_payload("xeviestudi", "xestud12345", "wpa"),
            "WIFI:S:xeviestudi;T:WPA;P:xestud12345;;",
        )

    def test_wep_payload(self):
        self.assertEqual(
            build_wifi_payload("red", "clave123", "wep"),
            "WIFI:S:red;T:WEP;P:clave123;;",
        )

    def test_none_payload_without_password(self):
        self.assertEqual(
            build_wifi_payload("red_abierta", "", "none"),
            "WIFI:S:red_abierta;T:NONE;P:;;",
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run python -m unittest -v`
Expected: FAIL with `ImportError: cannot import name 'build_wifi_payload' from 'main'` (test module errors during import).

- [ ] **Step 3: Write minimal implementation**

Add this function to `main.py` (after the `import qrcode` line, before `def main():`):

```python
def build_wifi_payload(ssid: str, password: str, enc_type: str) -> str:
    return f"WIFI:S:{ssid};T:{enc_type.upper()};P:{password};;"
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run python -m unittest -v`
Expected: PASS, 3 tests.

- [ ] **Step 5: Commit**

```bash
git add tests/test_main.py main.py
git commit -m "Add build_wifi_payload with tests"
```

---

### Task 2: CLI arguments + remove hardcoded credentials (TDD)

**Files:**
- Modify: `tests/test_main.py` (add CLI test class; full file shown)
- Modify: `main.py` (rewrite `main()`; final file shown)

**Interfaces:**
- Consumes: `build_wifi_payload(ssid, password, enc_type) -> str` from Task 1.
- Produces: `main(argv: list[str] | None = None) -> None` — parses `--ssid` (required), `--password` (optional, required at runtime for `wpa`/`wep`), `--type` (`wpa`|`wep`|`none`, default `wpa`), `-o/--output` (default `codigo_qr.png`); raises `SystemExit(2)` via `parser.error` when password is missing for `wpa`/`wep`.

- [ ] **Step 1: Write the failing tests**

Replace `tests/test_main.py` with:

```python
import os
import tempfile
import unittest
from pathlib import Path

import main as main_module
from main import build_wifi_payload, main


class BuildWifiPayloadTestCase(unittest.TestCase):
    def test_wpa_payload_matches_legacy_format(self):
        self.assertEqual(
            build_wifi_payload("xeviestudi", "xestud12345", "wpa"),
            "WIFI:S:xeviestudi;T:WPA;P:xestud12345;;",
        )

    def test_wep_payload(self):
        self.assertEqual(
            build_wifi_payload("red", "clave123", "wep"),
            "WIFI:S:red;T:WEP;P:clave123;;",
        )

    def test_none_payload_without_password(self):
        self.assertEqual(
            build_wifi_payload("red_abierta", "", "none"),
            "WIFI:S:red_abierta;T:NONE;P:;;",
        )


class MainCliTestCase(unittest.TestCase):
    def test_generates_qr_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "out.png")
            main(["--ssid", "MiRed", "--password", "supersegura", "-o", out])
            self.assertTrue(os.path.exists(out))

    def test_missing_password_for_wpa_exits_with_error(self):
        with self.assertRaises(SystemExit) as ctx:
            main(["--ssid", "MiRed", "--type", "wpa"])
        self.assertEqual(ctx.exception.code, 2)

    def test_none_type_without_password_succeeds(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "out.png")
            main(["--ssid", "red_abierta", "--type", "none", "-o", out])
            self.assertTrue(os.path.exists(out))

    def test_no_hardcoded_credentials_in_source(self):
        source = Path(main_module.__file__).read_text(encoding="utf-8")
        self.assertNotIn("xeviestudi", source)
        self.assertNotIn("xestud12345", source)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run python -m unittest -v`
Expected: the 3 `MainCliTestCase` tests FAIL — `main()` called with an argument raises `TypeError: main() takes 0 positional arguments but 1 was given`, and `test_no_hardcoded_credentials_in_source` fails because the credentials are still in `main.py`. The 3 payload tests still pass.

- [ ] **Step 3: Rewrite `main.py`**

Replace the entire contents of `main.py` with:

```python
import argparse

import qrcode


def build_wifi_payload(ssid: str, password: str, enc_type: str) -> str:
    return f"WIFI:S:{ssid};T:{enc_type.upper()};P:{password};;"


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
```

Note: this also drops the leftover `print("Hello from qr!")` line, which is part of replacing the hardcoded main().

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run python -m unittest -v`
Expected: PASS, 7 tests.

- [ ] **Step 5: Manual smoke test**

Run: `uv run python main.py --ssid xeviestudi --password xestud12345`
Expected: prints `Código QR generado exitosamente en codigo_qr.png.` and rewrites `codigo_qr.png`.

Run: `uv run python main.py --ssid MiRed`
Expected: usage message plus `error: --password es obligatorio cuando --type es wpa`, exit code 2 (verify with `echo $?`).

- [ ] **Step 6: Commit**

```bash
git add tests/test_main.py main.py
git commit -m "Replace hardcoded credentials with CLI arguments"
```
