import unittest

from app.data.validator import validate_domain, validate_ip, validate_ips, validate_network_port, \
                               validate_http_response_code


class ValidateDomain(unittest.TestCase):
    def test_start_with_dot(self):
        """
        Test behavior of function check_domain_correctness when domain starts with dot
        :return:
        """
        self.assertEqual(validate_domain(domain=".test"), False)

    def test_start_with_hyphen(self):
        """
        Test behavior of function check_domain_correctness when domain starts with hyphen
        :return:
        """
        self.assertEqual(validate_domain(domain="-test"), False)

    def test_end_with_dot(self):
        """
        Test behavior of function check_domain_correctness when domain ends with dot
        :return:
        """
        self.assertEqual(validate_domain(domain="test."), False)

    def test_end_with_hyphen(self):
        """
        Test behavior of function check_domain_correctness when domain ends with hyphen
        :return:
        """
        self.assertEqual(validate_domain(domain="test-"), False)

    def test_start_end_with_dot(self):
        """
        Test behavior of function check_domain_correctness when domain starts and ends with dot
        :return:
        """
        self.assertEqual(validate_domain(domain=".test."), False)

    def test_start_end_with_hyphen(self):
        """
        Test behavior of function check_domain_correctness when domain starts and ends with hyphen
        :return:
        """
        self.assertEqual(validate_domain(domain="-test-"), False)

    def test_end_with_dot_end_with_hyphen(self):
        """
        Test behavior of function check_domain_correctness when domain starts with dot and ends with hyphen
        :return:
        """
        self.assertEqual(validate_domain(domain=".test-"), False)

    def test_start_with_hyphen_end_with_dot(self):
        """
        Test behavior of function check_domain_correctness when domain starts with hyphen and ends with dot
        :return:
        """
        self.assertEqual(validate_domain(domain="-test."), False)

    def test_start_with_dot_hyphen(self):
        """
        Test behavior of function check_domain_correctness when domain starts with dot and next char is hyphen
        :return:
        """
        self.assertEqual(validate_domain(domain=".-test"), False)

    def test_start_with_hyphen_dot(self):
        """
        Test behavior of function check_domain_correctness when domain starts with hyphen and next char is dot
        :return:
        """
        self.assertEqual(validate_domain(domain="-.test"), False)

    def test_end_with_dot_hyphen(self):
        """
        Test behavior of function check_domain_correctness when domain ends with dot and next char is hyphen
        :return:
        """
        self.assertEqual(validate_domain(domain="test.-"), False)

    def test_end_with_hyphen_dot(self):
        """
        Test behavior of function check_domain_correctness when domain ends with hyphen and next char is dot
        :return:
        """
        self.assertEqual(validate_domain(domain="test-."), False)

    def test_start_with_dot_hyphen_end_with_hyphen_dot(self):
        """
        Test behavior of function check_domain_correctness when domain starts with '.-' and ends with '-.'
        :return:
        """
        self.assertEqual(validate_domain(domain=".-test-."), False)

    def start_with_hyphen_dot_end_with_dot_hyphen(self):
        """
        Test behavior of function check_domain_correctness when domain starts with '-.' and ends with '.-'
        :return:
        """
        self.assertEqual(validate_domain(domain="-.test.-"), False)

    def test_start_with_dot_hyphen_end_with_dot_hyphen(self):
        """
        Test behavior of function check_domain_correctness when domain starts with '.-' and ends with '.-'
        :return:
        """
        self.assertEqual(validate_domain(domain=".-test.-"), False)

    def test_start_with_hyphen_dot_end_with_hyphen_dot(self):
        """
        Test behavior of function check_domain_correctness when domain starts with '-.' and ends with '-.'
        :return:
        """
        self.assertEqual(validate_domain(domain="-.test-."), False)

    def test_start_with_hyphen_hyphen(self):
        """
        Test behavior of function check_domain_correctness when domain starts with double hyphen
        :return:
        """
        self.assertEqual(validate_domain(domain="--test"), False)

    def test_start_with_dot_dot(self):
        """
        Test behavior of function check_domain_correctness when domain starts with double dot
        :return:
        """
        self.assertEqual(validate_domain(domain="..test"), False)

    def test_end_with_hyphen_hyphen(self):
        """
        Test behavior of function check_domain_correctness when domain ends with double hyphen
        :return:
        """
        self.assertEqual(validate_domain(domain="test--"), False)

    def test_end_with_dot_dot(self):
        """
        Test behavior of function check_domain_correctness when domain ends with double dot
        :return:
        """
        self.assertEqual(validate_domain(domain="test.."), False)

    def test_start_with_hyphen_hyphen_end_with_hyphen_hyphen(self):
        """
        Test behavior of function check_domain_correctness when domain starts and stop with double hyphen
        :return:
        """
        self.assertEqual(validate_domain(domain="--test--"), False)

    def test_start_with_dot_dot_end_with_dot_dot(self):
        """
        Test behavior of function check_domain_correctness when domain starts and stop with double hyphen dot
        :return:
        """
        self.assertEqual(validate_domain(domain="..test.."), False)

    def test_dot_inside(self):
        """
        Test behavior of function check_domain_correctness when dot is inside domain
        :return:
        """
        self.assertEqual(validate_domain(domain="test.test"), True)

    def test_multiple_dot_inside(self):
        """
        Test behavior of function check_domain_correctness when there is more than one dot is inside domain
        :return:
        """
        self.assertEqual(validate_domain(domain="test.other.test"), True)
        self.assertEqual(validate_domain(domain="test.other.test.test"), True)
        self.assertEqual(validate_domain(domain="adguard.example.com"), True)

    def test_dot_inside_start_with_dot(self):
        """
        Test behavior of function check_domain_correctness when dot is inside domain and domain starts with dot
        :return:
        """
        self.assertEqual(validate_domain(domain=".test.test"), False)

    def test_dot_inside_end_with_dot(self):
        """
        Test behavior of function check_domain_correctness when dot is inside domain and domain ends with dot
        :return:
        """
        self.assertEqual(validate_domain(domain="test.test."), False)

    def test_dot_inside_start_with_dot_end_with_dot(self):
        """
        Test behavior of function check_domain_correctness when dot is inside domain; domain starts and ends with dot
        :return:
        """
        self.assertEqual(validate_domain(domain=".test.test."), False)

    def test_multiple_dot_inside_start_with_dot(self):
        """
        Test behavior of function check_domain_correctness when there is more than one dot  inside domain
        and domain starts with dot
        :return:
        """
        self.assertEqual(validate_domain(domain=".test.test"), False)

    def test_multiple_dot_inside_end_with_dot(self):
        """
        Test behavior of function check_domain_correctness when there is more than one dot is inside domain
        and domain ends with dot
        :return:
        """
        self.assertEqual(validate_domain(domain="test.test."), False)

    def test_multiple_dot_inside_start_with_dot_end_with_dot(self):
        """
        Test behavior of function check_domain_correctness when there is more than one dot is inside domain,
        domain starts and ends with dot
        :return:
        """
        self.assertEqual(validate_domain(domain=".test.test."), False)

    def test_length_domain_extension(self):
        """
        Test behavior of function check_domain_correctness when domain length of extension is <= 4
        """
        self.assertEqual(validate_domain(domain="test.abcd"), True)
        self.assertEqual(validate_domain(domain="test.abc"), True)
        self.assertEqual(validate_domain(domain="test.ab"), True)
        self.assertEqual(validate_domain(domain="test.a"), True)

    def test_length_domain_extension_to_long(self):
        """
        Test behavior of function check_domain_correctness when  length of domain extension is > 4
        """
        self.assertEqual(validate_domain(domain="test.abcde"), False)

    def test_length_domain_extension_multiple_extensions(self):
        """
        Test behavior of function check_domain_correctness when length of domain extension is <= 4, but domain contains
        multiple extensions
        """
        self.assertEqual(validate_domain(domain="test.abcd.qwer"), True)
        self.assertEqual(validate_domain(domain="test.abcd.qwer.zxcv"), True)
        self.assertEqual(validate_domain(domain="a.b.c.d.e.f.g.h.i"), True)

    def test_length_domain(self):
        """
        Test behavior of function check_domain_correctness when domain length is <= 63
        :return:
        """
        # 63 char domain
        self.assertEqual(validate_domain(domain=
                                         "recite-rocking-irritably-threefold-enjoying-engross-unlock.com"),
                         True)

    def test_length_domain_to_long(self):
        """
        Test behavior of function check_domain_correctness when domain length is > 63
        :return:
        """
        # 63 char domain
        self.assertEqual(validate_domain(domain=
                                         "recite-rocking-irritably-threefold-enjoying-engross-unlock-sel.com"),
                         False)

    def test_dot_next_to_each_other(self):
        """
        Test behavior of function check_domain_correctness when domain contains two or more dots which occur next to
        each others
        :return:
        """
        self.assertEqual(validate_domain(domain="test..test"), False)
        self.assertEqual(validate_domain(domain="test.test"), True)
        self.assertEqual(validate_domain(domain="test...test"), False)

    def test_domain_correct(self):
        """
        Test behavior of function check_domain_correctness when domain contains only valid chars
        :return:
        """
        self.assertEqual(validate_domain(domain="example.com"), True)
        self.assertEqual(validate_domain(domain="example-next.com"), True)
        self.assertEqual(validate_domain(domain="subdomain.example.com"), True)
        self.assertEqual(validate_domain(domain="subdomain.example.org.com"), True)
        self.assertEqual(validate_domain(domain="example.org.com"), True)
        self.assertEqual(validate_domain(domain="example12.org.com"), True)

    def test_domain_colon_semicolon(self):
        """
        Test behavior of function check_domain_correctness when domain contains colon or semicolon
        :return:
        """
        self.assertEqual(validate_domain(domain="example:.com"), False)
        self.assertEqual(validate_domain(domain=":example.com"), False)
        self.assertEqual(validate_domain(domain=":example:.com"), False)
        self.assertEqual(validate_domain(domain="example:page.com"), False)
        self.assertEqual(validate_domain(domain="example;.com"), False)
        self.assertEqual(validate_domain(domain=";example.com"), False)
        self.assertEqual(validate_domain(domain=";example;.com"), False)
        self.assertEqual(validate_domain(domain="example;page.com"), False)
        self.assertEqual(validate_domain(domain=":"), False)
        self.assertEqual(validate_domain(domain=";"), False)

    def test_domain_brackets(self):
        """
        Test behavior of function check_domain_correctness when domain contains brackets
        :return:
        """
        self.assertEqual(validate_domain(domain="example{}test.com"), False)
        self.assertEqual(validate_domain(domain="{example}.com"), False)
        self.assertEqual(validate_domain(domain="{.com"), False)
        self.assertEqual(validate_domain(domain="}.com"), False)
        self.assertEqual(validate_domain(domain="example[]test.com"), False)
        self.assertEqual(validate_domain(domain="[example].com"), False)
        self.assertEqual(validate_domain(domain="[.com"), False)
        self.assertEqual(validate_domain(domain="].com"), False)
        self.assertEqual(validate_domain(domain="example()test.com"), False)
        self.assertEqual(validate_domain(domain="(example).com"), False)
        self.assertEqual(validate_domain(domain="(.com"), False)
        self.assertEqual(validate_domain(domain=").com"), False)

    def test_domain_math_symbols(self):
        """brackets
        Test behavior of function check_domain_correctness when domain contains math symbols
        :return:
        """
        self.assertEqual(validate_domain(domain="example+test.com"), False)
        self.assertEqual(validate_domain(domain="+example.com"), False)
        self.assertEqual(validate_domain(domain="example.com+"), False)
        self.assertEqual(validate_domain(domain="+example.com+"), False)

        self.assertEqual(validate_domain(domain="example=test.com"), False)
        self.assertEqual(validate_domain(domain="example.com="), False)
        self.assertEqual(validate_domain(domain="=example.com"), False)
        self.assertEqual(validate_domain(domain="=example.com="), False)

        self.assertEqual(validate_domain(domain="example/test.com"), False)
        self.assertEqual(validate_domain(domain="/example.com"), False)
        self.assertEqual(validate_domain(domain="example.com/"), False)
        self.assertEqual(validate_domain(domain="/example.com/"), False)

        self.assertEqual(validate_domain(domain="example*test.com"), False)
        self.assertEqual(validate_domain(domain="*example.com"), False)
        self.assertEqual(validate_domain(domain="example.com*"), False)
        self.assertEqual(validate_domain(domain="*example.com*"), False)

        self.assertEqual(validate_domain(domain="example%test.com"), False)
        self.assertEqual(validate_domain(domain="example.com%"), False)
        self.assertEqual(validate_domain(domain="%example.com"), False)
        self.assertEqual(validate_domain(domain="%example.com%"), False)

    def test_domain_quotes_single(self):
        """
        Test behavior of function check_domain_correctness when domain contains quotes
        :return:
        """
        self.assertEqual(validate_domain(domain="'example.com'"), False)
        self.assertEqual(validate_domain(domain="'example.com"), False)
        self.assertEqual(validate_domain(domain="example.com'"), False)
        self.assertEqual(validate_domain(domain="example'.com"), False)

    def test_domain_quotes_double(self):
        """
        Test behavior of function check_domain_correctness when domain contains quotes
        :return:
        """
        self.assertEqual(validate_domain(domain='"example.com"'), False)
        self.assertEqual(validate_domain(domain='"example.com'), False)
        self.assertEqual(validate_domain(domain='example.com"'), False)
        self.assertEqual(validate_domain(domain='example".com'), False)

    def test_domain_quotes(self):
        """
        Test behavior of function check_domain_correctness when domain contains quotes
        :return:
        """
        self.assertEqual(validate_domain(domain="`example.com`"), False)
        self.assertEqual(validate_domain(domain="`example.com"), False)
        self.assertEqual(validate_domain(domain="example.com`"), False)
        self.assertEqual(validate_domain(domain="example`.com"), False)

        self.assertEqual(validate_domain(domain="<example.com>"), False)
        self.assertEqual(validate_domain(domain="<example.com"), False)
        self.assertEqual(validate_domain(domain="example.com>"), False)
        self.assertEqual(validate_domain(domain="example>.com"), False)

        self.assertEqual(validate_domain(domain="<example.com<"), False)
        self.assertEqual(validate_domain(domain="example.com<"), False)
        self.assertEqual(validate_domain(domain="<example.com"), False)
        self.assertEqual(validate_domain(domain="example<.com"), False)

    def test_domain_special_chars(self):
        """brackets
        Test behavior of function check_domain_correctness when domain contains special chars
        :return:
        """
        self.assertEqual(validate_domain(domain="@example.com@"), False)
        self.assertEqual(validate_domain(domain="@example.com@"), False)
        self.assertEqual(validate_domain(domain="@example.com@"), False)
        self.assertEqual(validate_domain(domain="@example.com@"), False)

        self.assertEqual(validate_domain(domain="#example.com#"), False)
        self.assertEqual(validate_domain(domain="example.com#"), False)
        self.assertEqual(validate_domain(domain="#example.com"), False)
        self.assertEqual(validate_domain(domain="example#.com"), False)

        self.assertEqual(validate_domain(domain="$example.com$"), False)
        self.assertEqual(validate_domain(domain="example.com$"), False)
        self.assertEqual(validate_domain(domain="$example.com"), False)
        self.assertEqual(validate_domain(domain="example$.com"), False)

        self.assertEqual(validate_domain(domain="^example.com^"), False)
        self.assertEqual(validate_domain(domain="example.com^"), False)
        self.assertEqual(validate_domain(domain="^example.com"), False)
        self.assertEqual(validate_domain(domain="example^.com"), False)

        self.assertEqual(validate_domain(domain="&example.com&"), False)
        self.assertEqual(validate_domain(domain="example.com&"), False)
        self.assertEqual(validate_domain(domain="&example.com"), False)
        self.assertEqual(validate_domain(domain="example&.com"), False)

        self.assertEqual(validate_domain(domain="_example.com_"), False)
        self.assertEqual(validate_domain(domain="example.com_"), False)
        self.assertEqual(validate_domain(domain="_example.com"), False)
        self.assertEqual(validate_domain(domain="example_.com"), False)


class ValidateIP(unittest.TestCase):
    def test_ipv4_class_A(self):
        self.assertEqual(validate_ip(ip="1.0.0.0"), True)
        self.assertEqual(validate_ip(ip="2.2.2.2"), True)
        self.assertEqual(validate_ip(ip="127.0.0.0"), True)

        self.assertEqual(validate_ip(ip="10.0.0.0"), True)
        self.assertEqual(validate_ip(ip="10.13.32.2"), True)
        self.assertEqual(validate_ip(ip="10.255.255.255"), True)

    def test_ipv4_class_B(self):
        self.assertEqual(validate_ip(ip="128.0.0.0"), True)
        self.assertEqual(validate_ip(ip="191.23.12.0"), True)
        self.assertEqual(validate_ip(ip="191.255.0.0"), True)

        self.assertEqual(validate_ip(ip="172.16.0.0"), True)
        self.assertEqual(validate_ip(ip="172.16.23.0"), True)
        self.assertEqual(validate_ip(ip="172.31.255.255"), True)

    def test_ipv4_class_C(self):
        self.assertEqual(validate_ip(ip="192.0.0.0"), True)
        self.assertEqual(validate_ip(ip="192.23.0.0"), True)
        self.assertEqual(validate_ip(ip="223.255.255.0"), True)

        self.assertEqual(validate_ip(ip="192.168.0.0"), True)
        self.assertEqual(validate_ip(ip="192.168.1.1"), True)
        self.assertEqual(validate_ip(ip="192.168.255.255"), True)

    def test_ipv4_class_wrong(self):
        self.assertEqual(validate_ip(ip="s.0.0.0"), False)
        self.assertEqual(validate_ip(ip="999.999.999.999"), False)
        self.assertEqual(validate_ip(ip="-999.999.999.999"), False)
        self.assertEqual(validate_ip(ip="23"), False)


class ValidateNetworkPort(unittest.TestCase):
    def test_port_under_range(self):
        self.assertEqual(validate_network_port(-102), False)

    def test_port_over_range(self):
        self.assertEqual(validate_network_port(70000), False)

    def test_port_lowest_value(self):
        self.assertEqual(validate_network_port(0), True)

    def test_port_highest_value(self):
        self.assertEqual(validate_network_port(65535), True)


class ValidateHttpResponseCode(unittest.TestCase):
    def test_negative_code(self):
        """
        Test behavior of function ValidateHttpResponseCode when code is less than zero
        :return:
        """
        self.assertEqual(validate_http_response_code(code=-3), False)

    def test_zero_code(self):
        """
        Test behavior of function ValidateHttpResponseCode when code is zero
        :return:
        """
        self.assertEqual(validate_http_response_code(code=0), False)

    def test_ok_code(self):
        """
        Test behavior of function ValidateHttpResponseCode when code is correct
        :return:
        """
        self.assertEqual(validate_http_response_code(code=200), True)

    def test_code_to_high(self):
        """
        Test behavior of function ValidateHttpResponseCode when code is 600
        :return:
        """
        self.assertEqual(validate_http_response_code(code=600), False)


class ValidateIps(unittest.TestCase):
    def test_list_of_ip(self):
        self.assertEqual(validate_ips(ips=["10.2.3.12", "192.158.23.23"]), True)

    def test_empty_list(self):
        self.assertEqual(validate_ips(ips=[]), False)

    def test_list_of_invalid_ip(self):
        self.assertEqual(validate_ips(ips=["10.2.3.12", "192.q158.23.23"]), False)

    def test_string(self):
        self.assertEqual(validate_ips(ips="10.0.10.10"), True)

    def test_string_invalid_ip(self):
        self.assertEqual(validate_ips(ips="1q0.0.10.10"), False)


if __name__ == "__main__":
    unittest.main()
