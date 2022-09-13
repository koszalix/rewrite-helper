import unittest
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL

from app.utils import check_protocol_slashed
from app.utils import parse_value_with_default
from app.utils import check_linux_permissions
from app.utils import parse_logging_level
from app.utils import match_port_to_protocol


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

    def test_https_empty(self):
        self.assertEqual(check_protocol_slashed(""), "")


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


class ParseLoggingLevel(unittest.TestCase):
    def test_str_debug(self):
        self.assertEqual(parse_logging_level(logging_str="DEBUG"), DEBUG)

    def test_str_info(self):
        self.assertEqual(parse_logging_level(logging_str="INFO"), INFO)

    def test_str_warning(self):
        self.assertEqual(parse_logging_level(logging_str="WARNING"), WARNING)

    def test_str_error(self):
        self.assertEqual(parse_logging_level(logging_str="ERROR"), ERROR)

    def test_str_critical(self):
        self.assertEqual(parse_logging_level(logging_str="CRITICAL"), CRITICAL)

    def test_invalid_strint(self):
        self.assertEqual(parse_logging_level(logging_str="N/A"), False)
        self.assertEqual(parse_logging_level(logging_str="invalid-string"), False)

    def test_float(self):
        self.assertEqual(parse_logging_level(logging_str=3.14), False)
        self.assertEqual(parse_logging_level(logging_str=-3.14), False)

    def test_bool(self):
        self.assertEqual(parse_logging_level(logging_str=True), False)
        self.assertEqual(parse_logging_level(logging_str=False), False)

    def test_int(self):
        self.assertEqual(parse_logging_level(logging_str=3), False)
        self.assertEqual(parse_logging_level(logging_str=-3), False)


class MatchPortToProtocol(unittest.TestCase):
    def test_default(self):
        self.assertEqual(match_port_to_protocol(proto="test"), 80)

    def test_default_changed(self):
        self.assertEqual(match_port_to_protocol(proto="test", default_port=32), 32)

    def test_http(self):
        self.assertEqual(match_port_to_protocol(proto="http"), 80)

    def test_https(self):
        self.assertEqual(match_port_to_protocol(proto="tests"), 80)


if __name__ == '__main__':
    unittest.main()
