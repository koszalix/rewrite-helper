import unittest

from src.utils import check_protocol_slashed
from src.utils import parse_value_with_default
from src.utils import check_linux_permissions


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


class ParseValueWithDefault(unittest.TestCase):
    def test_key_in_content_value_assigned(self):
        content = {'key-a': 32, 'key-B': 33, 'key-c': 'key-B'}
        self.assertEqual(parse_value_with_default(content=content, key='key-B', default_value=80), 33)

    def test_key_in_content_value_assigned_strings(self):
        content = {'key-a': '32', 'key-B': '33', 'key-c': 'key-B'}
        self.assertEqual(parse_value_with_default(content=content, key='key-B', default_value='80'), '33')

    def test_default_value(self):
        content = {'key-a': '32', 'key-B': '33', 'key-c': 'key-b'}
        self.assertEqual(parse_value_with_default(content=content, key='key-t', default_value=80), 80)

    def test_default_value_strings(self):
        content = {'key-a': '32', 'key-B': '33', 'key-c': 'key-B'}
        self.assertEqual(parse_value_with_default(content=content, key='key-t', default_value='80'), '80')

    def test_content_is_none(self):
        content = None
        self.assertEqual(parse_value_with_default(content=content, key="test", default_value=80), 80)

    def test_key_value_is_none(self):
        content = {'key-x': 33, 'key-a': None}
        self.assertEqual(parse_value_with_default(content=content, key="key-a", default_value=80), 80)

    def test_type_int(self):
        content = {'key-a': '32', 'key-B': '33', 'key-c': 'key-B'}
        self.assertEqual(type(parse_value_with_default(content=content, key='key-B', default_value=80)), int)

    def test_type_float(self):
        content = {'key-a': '32', 'key-B': '33', 'key-c': 'key-B'}
        self.assertEqual(type(parse_value_with_default(content=content, key='key-B', default_value=80.0)), float)

    def test_type_bool(self):
        content = {'key-a': '32', 'key-B': '33', 'key-c': 'key-B'}
        self.assertEqual(type(parse_value_with_default(content=content, key='key-B', default_value=True)), bool)

    def test_type_string(self):
        content = {'key-a': '32', 'key-B': '33', 'key-c': 'key-B'}
        self.assertEqual(type(parse_value_with_default(content=content, key='key-B', default_value='80')), str)


class CheckLinuxPermissions(unittest.TestCase):
    def test_equal(self):
        self.assertEqual(check_linux_permissions("444", "444"), True)

    def test_permission_higher_than_target_first_char(self):
        self.assertEqual(check_linux_permissions("544", "444"), True)

    def test_permission_higher_than_target_second_char(self):
        self.assertEqual(check_linux_permissions("454", "444"), True)

    def test_permission_higher_than_target_third_char(self):
        self.assertEqual(check_linux_permissions("445", "444"), True)

    def test_permission_higher_than_target_1_2_char(self):
        self.assertEqual(check_linux_permissions("554", "444"), True)

    def test_permission_higher_than_target_2_3_char(self):
        self.assertEqual(check_linux_permissions("455", "444"), True)

    def test_permission_higher_than_target_1_3_char(self):
        self.assertEqual(check_linux_permissions("545", "444"), True)

    def test_permission_higher_than_target_all_char(self):
        self.assertEqual(check_linux_permissions("555", "444"), True)

    def test_permission_lower_than_target_first_char(self):
        self.assertEqual(check_linux_permissions("344", "444"), False)

    def test_permission_lower_than_target_second_char(self):
        self.assertEqual(check_linux_permissions("434", "444"), False)

    def test_permission_lower_than_target_third_char(self):
        self.assertEqual(check_linux_permissions("443", "444"), False)

    def test_permission_lower_than_target_1_2_char(self):
        self.assertEqual(check_linux_permissions("334", "444"), False)

    def test_permission_lower_than_target_2_3_char(self):
        self.assertEqual(check_linux_permissions("433", "444"), False)

    def test_permission_lower_than_target_1_3_char(self):
        self.assertEqual(check_linux_permissions("343", "444"), False)

    def test_permission_lower_than_target_all_char(self):
        self.assertEqual(check_linux_permissions("333", "444"), False)


if __name__ == '__main__':
    unittest.main()
