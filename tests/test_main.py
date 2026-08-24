import unittest

from main import build_wifi_payload


class BuildWifiPayloadTestCase(unittest.TestCase):
    def test_wpa_payload_matches_legacy_format(self):
        self.assertEqual(
            build_wifi_payload("my_wifi", "my_wifi_12345", "wpa"),
            "WIFI:S:my_wifi;T:WPA;P:my_wifi_12345;;",
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
