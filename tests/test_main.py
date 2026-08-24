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

    def test_ssid_with_special_characters_is_escaped(self):
        self.assertEqual(
            build_wifi_payload("My;Net,2", "clave123", "wpa"),
            "WIFI:S:My\\;Net\\,2;T:WPA;P:clave123;;",
        )

    def test_password_with_special_characters_is_escaped(self):
        self.assertEqual(
            build_wifi_payload("MiRed", "a:b\\c", "wpa"),
            "WIFI:S:MiRed;T:WPA;P:a\\:b\\\\c;;",
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
