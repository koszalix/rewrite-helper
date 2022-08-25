import unittest

from src.utils import check_protocol_slashed
from src.utils import safe_parse_value

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


class SafeParseValue(unittest.TestCase):
    def test_key_in_content_value_assigned(self):
        content = {'key-a': 32, 'key-B': 33, 'key-c': 'key-B'}
        self.assertEqual(safe_parse_value(content=content, key='key-b', default_value=80), 33)

    def test_key_in_content_value_assigned_strings(self):
        content = {'key-a': '32', 'key-B': '33', 'key-c': 'key-B'}
        self.assertEqual(safe_parse_value(content=content, key='key-B', default_value=80), '33')

    def test_default_value(self):
        content = {'key-a': '32', 'key-B': '33', 'key-c': 'key-b'}
        self.assertEqual(safe_parse_value(content=content, key='key-t', default_value=80), 80)

    def test_default_value_strings(self):
        content = {'key-a': '32', 'key-B': '33', 'key-c': 'key-B'}
        self.assertEqual(safe_parse_value(content=content, key='key-t', default_value='80'), '80')

if __name__ == '__main__':
    unittest.main()



