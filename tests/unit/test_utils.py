import unittest
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL

from src.utils import check_protocol_slashed
from src.utils import parse_value_with_default
from src.utils import check_linux_permissions
from src.utils import parse_logging_level
from src.utils import match_port_to_protocol
from src.utils import check_domain_correctness


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


class CheckDomainCorrectness(unittest.TestCase):
    def test_start_with_dot(self):
        """
        Test behavior of function check_domain_correctness when domain starts with dot
        :return:
        """
        self.assertEqual(check_domain_correctness(domain=".test"), False)

    def test_start_with_hyphen(self):
        """
        Test behavior of function check_domain_correctness when domain starts with hyphen
        :return:
        """
        self.assertEqual(check_domain_correctness(domain="-test"), False)

    def test_end_with_dot(self):
        """
        Test behavior of function check_domain_correctness when domain ends with dot
        :return:
        """
        self.assertEqual(check_domain_correctness(domain="test."), False)

    def test_end_with_hyphen(self):
        """
        Test behavior of function check_domain_correctness when domain ends with hyphen
        :return:
        """
        self.assertEqual(check_domain_correctness(domain="test-"), False)

    def test_start_end_with_dot(self):
        """
        Test behavior of function check_domain_correctness when domain starts and ends with dot
        :return:
        """
        self.assertEqual(check_domain_correctness(domain=".test."), False)

    def test_start_end_with_hyphen(self):
        """
        Test behavior of function check_domain_correctness when domain starts and ends with hyphen
        :return:
        """
        self.assertEqual(check_domain_correctness(domain="-test-"), False)

    def test_end_with_dot_end_with_hyphen(self):
        """
        Test behavior of function check_domain_correctness when domain starts with dot and ends with hyphen
        :return:
        """
        self.assertEqual(check_domain_correctness(domain=".test-"), False)

    def test_start_with_hyphen_end_with_dot(self):
        """
        Test behavior of function check_domain_correctness when domain starts with hyphen and ends with dot
        :return:
        """
        self.assertEqual(check_domain_correctness(domain="-test."), False)

    def test_start_with_dot_hyphen(self):
        """
        Test behavior of function check_domain_correctness when domain starts with dot and next char is hyphen
        :return:
        """
        self.assertEqual(check_domain_correctness(domain=".-test"), False)

    def test_start_with_hyphen_dot(self):
        """
        Test behavior of function check_domain_correctness when domain starts with hyphen and next char is dot
        :return:
        """
        self.assertEqual(check_domain_correctness(domain="-.test"), False)

    def test_end_with_dot_hyphen(self):
        """
        Test behavior of function check_domain_correctness when domain ends with dot and next char is hyphen
        :return:
        """
        self.assertEqual(check_domain_correctness(domain="test.-"), False)

    def test_end_with_hyphen_dot(self):
        """
        Test behavior of function check_domain_correctness when domain ends with hyphen and next char is dot
        :return:
        """
        self.assertEqual(check_domain_correctness(domain="test-."), False)

    def test_start_with_dot_hyphen_end_with_hyphen_dot(self):
        """
        Test behavior of function check_domain_correctness when domain starts with '.-' and ends with '-.'
        :return:
        """
        self.assertEqual(check_domain_correctness(domain=".-test-."), False)

    def start_with_hyphen_dot_end_with_dot_hyphen(self):
        """
        Test behavior of function check_domain_correctness when domain starts with '-.' and ends with '.-'
        :return:
        """
        self.assertEqual(check_domain_correctness(domain="-.test.-"), False)

    def test_start_with_dot_hyphen_end_with_dot_hyphen(self):
        """
        Test behavior of function check_domain_correctness when domain starts with '.-' and ends with '.-'
        :return:
        """
        self.assertEqual(check_domain_correctness(domain=".-test.-"), False)

    def test_start_with_hyphen_dot_end_with_hyphen_dot(self):
        """
        Test behavior of function check_domain_correctness when domain starts with '-.' and ends with '-.'
        :return:
        """
        self.assertEqual(check_domain_correctness(domain="-.test-."), False)

    def test_start_with_hyphen_hyphen(self):
        """
        Test behavior of function check_domain_correctness when domain starts with double hyphen
        :return:
        """
        self.assertEqual(check_domain_correctness(domain="--test"), False)

    def test_start_with_dot_dot(self):
        """
        Test behavior of function check_domain_correctness when domain starts with double dot
        :return:
        """
        self.assertEqual(check_domain_correctness(domain="..test"), False)

    def test_end_with_hyphen_hyphen(self):
        """
        Test behavior of function check_domain_correctness when domain ends with double hyphen
        :return:
        """
        self.assertEqual(check_domain_correctness(domain="test--"), False)

    def test_end_with_dot_dot(self):
        """
        Test behavior of function check_domain_correctness when domain ends with double dot
        :return:
        """
        self.assertEqual(check_domain_correctness(domain="test.."), False)

    def test_start_with_hyphen_hyphen_end_with_hyphen_hyphen(self):
        """
        Test behavior of function check_domain_correctness when domain starts and stop with double hyphen
        :return:
        """
        self.assertEqual(check_domain_correctness(domain="--test--"), False)

    def test_start_with_dot_dot_end_with_dot_dot(self):
        """
        Test behavior of function check_domain_correctness when domain starts and stop with double hyphen dot
        :return:
        """
        self.assertEqual(check_domain_correctness(domain="..test.."), False)

    def test_dot_inside(self):
        """
        Test behavior of function check_domain_correctness when dot is inside domain
        :return:
        """
        self.assertEqual(check_domain_correctness(domain="test.test"), True)

    def test_multiple_dot_inside(self):
        """
        Test behavior of function check_domain_correctness when there is more than one dot is inside domain
        :return:
        """
        self.assertEqual(check_domain_correctness(domain="test.other.test"), True)
        self.assertEqual(check_domain_correctness(domain="test.other.test.test"), True)

    def test_dot_inside_start_with_dot(self):
        """
        Test behavior of function check_domain_correctness when dot is inside domain and domain starts with dot
        :return:
        """
        self.assertEqual(check_domain_correctness(domain=".test.test"), False)

    def test_dot_inside_end_with_dot(self):
        """
        Test behavior of function check_domain_correctness when dot is inside domain and domain ends with dot
        :return:
        """
        self.assertEqual(check_domain_correctness(domain="test.test."), False)

    def test_dot_inside_start_with_dot_end_with_dot(self):
        """
        Test behavior of function check_domain_correctness when dot is inside domain; domain starts and ends with dot
        :return:
        """
        self.assertEqual(check_domain_correctness(domain=".test.test."), False)

    def test_multiple_dot_inside_start_with_dot(self):
        """
        Test behavior of function check_domain_correctness when there is more than one dot  inside domain
        and domain starts with dot
        :return:
        """
        self.assertEqual(check_domain_correctness(domain=".test.test"), False)

    def test_multiple_dot_inside_end_with_dot(self):
        """
        Test behavior of function check_domain_correctness when there is more than one dot is inside domain
        and domain ends with dot
        :return:
        """
        self.assertEqual(check_domain_correctness(domain="test.test."), False)

    def test_multiple_dot_inside_start_with_dot_end_with_dot(self):
        """
        Test behavior of function check_domain_correctness when there is more than one dot is inside domain,
        domain starts and ends with dot
        :return:
        """
        self.assertEqual(check_domain_correctness(domain=".test.test."), False)

    def test_length_domain_extension(self):
        """
        Test behavior of function check_domain_correctness when domain length of extension is <= 4
        """
        self.assertEqual(check_domain_correctness(domain="test.abcd"), True)
        self.assertEqual(check_domain_correctness(domain="test.abc"), True)
        self.assertEqual(check_domain_correctness(domain="test.ab"), True)
        self.assertEqual(check_domain_correctness(domain="test.a"), True)

    def test_length_domain_extension_to_long(self):
        """
        Test behavior of function check_domain_correctness when  length of domain extension is > 4
        """
        self.assertEqual(check_domain_correctness(domain="test.abcde"), False)

    def test_length_domain_extension_multiple_extensions(self):
        """
        Test behavior of function check_domain_correctness when length of domain extension is <= 4, but domain contains
        multiple extensions
        """
        self.assertEqual(check_domain_correctness(domain="test.abcd.qwer"), True)
        self.assertEqual(check_domain_correctness(domain="test.abcd.qwer.zxcv"), True)
        self.assertEqual(check_domain_correctness(domain="a.b.c.d.e.f.g.h.i"), True)

    def test_length_domain(self):
        """
        Test behavior of function check_domain_correctness when domain length is <= 63
        :return:
        """
        # 63 char domain
        self.assertEqual(check_domain_correctness(domain=
                                                  "recite-rocking-irritably-threefold-enjoying-engross-unlock.com"),
                         True)

    def test_length_domain_to_long(self):
        """
        Test behavior of function check_domain_correctness when domain length is > 63
        :return:
        """
        # 63 char domain
        self.assertEqual(check_domain_correctness(domain=
                                                  "recite-rocking-irritably-threefold-enjoying-engross-unlock-sel.com"),
                         False)

    def test_dot_next_to_each_other(self):
        """
        Test behavior of function check_domain_correctness when domain contains two or more dots which occur next to
        each others
        :return:
        """
        self.assertEqual(check_domain_correctness(domain="test..test"), False)
        self.assertEqual(check_domain_correctness(domain="test.test"), True)
        self.assertEqual(check_domain_correctness(domain="test...test"), False)

    def test_domain_correct(self):
        """
        Test behavior of function check_domain_correctness when domain contains only valid chars
        :return:
        """
        self.assertEqual(check_domain_correctness(domain="example.com"), True)
        self.assertEqual(check_domain_correctness(domain="example-next.com"), True)
        self.assertEqual(check_domain_correctness(domain="subdomain.example.com"), True)
        self.assertEqual(check_domain_correctness(domain="subdomain.example.org.com"), True)
        self.assertEqual(check_domain_correctness(domain="example.org.com"), True)
        self.assertEqual(check_domain_correctness(domain="example12.org.com"), True)

    def test_domain_colon_semicolon(self):
        """
        Test behavior of function check_domain_correctness when domain contains colon or semicolon
        :return:
        """
        self.assertEqual(check_domain_correctness(domain="example:.com"), False)
        self.assertEqual(check_domain_correctness(domain=":example.com"), False)
        self.assertEqual(check_domain_correctness(domain=":example:.com"), False)
        self.assertEqual(check_domain_correctness(domain="example:page.com"), False)
        self.assertEqual(check_domain_correctness(domain="example;.com"), False)
        self.assertEqual(check_domain_correctness(domain=";example.com"), False)
        self.assertEqual(check_domain_correctness(domain=";example;.com"), False)
        self.assertEqual(check_domain_correctness(domain="example;page.com"), False)
        self.assertEqual(check_domain_correctness(domain=":"), False)
        self.assertEqual(check_domain_correctness(domain=";"), False)

    def test_domain_brackets(self):
        """
        Test behavior of function check_domain_correctness when domain contains brackets
        :return:
        """
        self.assertEqual(check_domain_correctness(domain="example{}test.com"), False)
        self.assertEqual(check_domain_correctness(domain="{example}.com"), False)
        self.assertEqual(check_domain_correctness(domain="{.com"), False)
        self.assertEqual(check_domain_correctness(domain="}.com"), False)
        self.assertEqual(check_domain_correctness(domain="example[]test.com"), False)
        self.assertEqual(check_domain_correctness(domain="[example].com"), False)
        self.assertEqual(check_domain_correctness(domain="[.com"), False)
        self.assertEqual(check_domain_correctness(domain="].com"), False)
        self.assertEqual(check_domain_correctness(domain="example()test.com"), False)
        self.assertEqual(check_domain_correctness(domain="(example).com"), False)
        self.assertEqual(check_domain_correctness(domain="(.com"), False)
        self.assertEqual(check_domain_correctness(domain=").com"), False)

    def test_domain_math_symbols(self):
        """brackets
        Test behavior of function check_domain_correctness when domain contains math symbols
        :return:
        """
        self.assertEqual(check_domain_correctness(domain="example+test.com"), False)
        self.assertEqual(check_domain_correctness(domain="+example.com"), False)
        self.assertEqual(check_domain_correctness(domain="example.com+"), False)
        self.assertEqual(check_domain_correctness(domain="+example.com+"), False)

        self.assertEqual(check_domain_correctness(domain="example=test.com"), False)
        self.assertEqual(check_domain_correctness(domain="example.com="), False)
        self.assertEqual(check_domain_correctness(domain="=example.com"), False)
        self.assertEqual(check_domain_correctness(domain="=example.com="), False)

        self.assertEqual(check_domain_correctness(domain="example/test.com"), False)
        self.assertEqual(check_domain_correctness(domain="/example.com"), False)
        self.assertEqual(check_domain_correctness(domain="example.com/"), False)
        self.assertEqual(check_domain_correctness(domain="/example.com/"), False)

        self.assertEqual(check_domain_correctness(domain="example*test.com"), False)
        self.assertEqual(check_domain_correctness(domain="*example.com"), False)
        self.assertEqual(check_domain_correctness(domain="example.com*"), False)
        self.assertEqual(check_domain_correctness(domain="*example.com*"), False)

        self.assertEqual(check_domain_correctness(domain="example%test.com"), False)
        self.assertEqual(check_domain_correctness(domain="example.com%"), False)
        self.assertEqual(check_domain_correctness(domain="%example.com"), False)
        self.assertEqual(check_domain_correctness(domain="%example.com%"), False)

    def test_domain_quotes_single(self):
        """
        Test behavior of function check_domain_correctness when domain contains quotes
        :return:
        """
        self.assertEqual(check_domain_correctness(domain="'example.com'"), False)
        self.assertEqual(check_domain_correctness(domain="'example.com"), False)
        self.assertEqual(check_domain_correctness(domain="example.com'"), False)
        self.assertEqual(check_domain_correctness(domain="example'.com"), False)

    def test_domain_quotes_double(self):
        """
        Test behavior of function check_domain_correctness when domain contains quotes
        :return:
        """
        self.assertEqual(check_domain_correctness(domain='"example.com"'), False)
        self.assertEqual(check_domain_correctness(domain='"example.com'), False)
        self.assertEqual(check_domain_correctness(domain='example.com"'), False)
        self.assertEqual(check_domain_correctness(domain='example".com'), False)

    def test_domain_quotes(self):
        """
        Test behavior of function check_domain_correctness when domain contains quotes
        :return:
        """
        self.assertEqual(check_domain_correctness(domain="`example.com`"), False)
        self.assertEqual(check_domain_correctness(domain="`example.com"), False)
        self.assertEqual(check_domain_correctness(domain="example.com`"), False)
        self.assertEqual(check_domain_correctness(domain="example`.com"), False)

        self.assertEqual(check_domain_correctness(domain="<example.com>"), False)
        self.assertEqual(check_domain_correctness(domain="<example.com"), False)
        self.assertEqual(check_domain_correctness(domain="example.com>"), False)
        self.assertEqual(check_domain_correctness(domain="example>.com"), False)

        self.assertEqual(check_domain_correctness(domain="<example.com<"), False)
        self.assertEqual(check_domain_correctness(domain="example.com<"), False)
        self.assertEqual(check_domain_correctness(domain="<example.com"), False)
        self.assertEqual(check_domain_correctness(domain="example<.com"), False)

    def test_domain_special_chars(self):

        """brackets
        Test behavior of function check_domain_correctness when domain contains special chars
        :return:
        """
        self.assertEqual(check_domain_correctness(domain="@example.com@"), False)
        self.assertEqual(check_domain_correctness(domain="@example.com@"), False)
        self.assertEqual(check_domain_correctness(domain="@example.com@"), False)
        self.assertEqual(check_domain_correctness(domain="@example.com@"), False)

        self.assertEqual(check_domain_correctness(domain="#example.com#"), False)
        self.assertEqual(check_domain_correctness(domain="example.com#"), False)
        self.assertEqual(check_domain_correctness(domain="#example.com"), False)
        self.assertEqual(check_domain_correctness(domain="example#.com"), False)

        self.assertEqual(check_domain_correctness(domain="$example.com$"), False)
        self.assertEqual(check_domain_correctness(domain="example.com$"), False)
        self.assertEqual(check_domain_correctness(domain="$example.com"), False)
        self.assertEqual(check_domain_correctness(domain="example$.com"), False)

        self.assertEqual(check_domain_correctness(domain="^example.com^"), False)
        self.assertEqual(check_domain_correctness(domain="example.com^"), False)
        self.assertEqual(check_domain_correctness(domain="^example.com"), False)
        self.assertEqual(check_domain_correctness(domain="example^.com"), False)

        self.assertEqual(check_domain_correctness(domain="&example.com&"), False)
        self.assertEqual(check_domain_correctness(domain="example.com&"), False)
        self.assertEqual(check_domain_correctness(domain="&example.com"), False)
        self.assertEqual(check_domain_correctness(domain="example&.com"), False)

        self.assertEqual(check_domain_correctness(domain="_example.com_"), False)
        self.assertEqual(check_domain_correctness(domain="example.com_"), False)
        self.assertEqual(check_domain_correctness(domain="_example.com"), False)
        self.assertEqual(check_domain_correctness(domain="example_.com"), False)


if __name__ == '__main__':
    unittest.main()
