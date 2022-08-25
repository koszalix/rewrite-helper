import unittest

from src.utils import check_protocol_slashed

class CheckProtocolSlashed(unittest.TestCase):
    def test_http_slashed(self):
        self.assertEqual(check_protocol_slashed("http://"), "http://")

    def test_http_not_slashed(self):
        self.assertEqual(check_protocol_slashed("http"), "http://")

    def test_http_colon_only(self):
        self.assertEqual(check_protocol_slashed("http:"), "http://")

    def test_http_single_slash(self):
        self.assertEqual(check_protocol_slashed("http:/"), "http://")

    def test_https_slashed(self):
        self.assertEqual(check_protocol_slashed("https://"), "https://")

    def test_https_not_slashed(self):
        self.assertEqual(check_protocol_slashed("https"), "https://")

    def test_https_colon_only(self):
        self.assertEqual(check_protocol_slashed("https:"), "https://")

    def test_https_single_slash(self):
        self.assertEqual(check_protocol_slashed("https:/"), "https://")

if __name__ == '__main__':
    unittest.main()



