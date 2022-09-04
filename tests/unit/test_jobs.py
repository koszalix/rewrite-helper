import logging
import unittest

from src.jobs import ping
from src.jobs import http
from src.jobs import static_entry
from src.static import data


class TestPing(unittest.TestCase):

    def setUp(self):
        self.ping = ping.Test(count=2, timeout=0.2, dns_domain="test.lan", api_connect=None,
                              dns_answer="192.168.56.105", interval=10, dns_answer_failover=["192.168.56.22"])

        self.ping_negative_count = ping.Test(count=2, timeout=0.2, dns_domain="test.lan", api_connect=None,
                                             dns_answer="192.168.56.105", interval=10,
                                             dns_answer_failover=["192.168.56.22"])
        self.ping_zero_count = ping.Test(count=2, timeout=0.2, dns_domain="test.lan", api_connect=None,
                                         dns_answer="192.168.56.105", interval=10,
                                         dns_answer_failover=["192.168.56.22"])

        self.ping_negative_timeout = ping.Test(count=2, timeout=-4, dns_domain="test.lan", api_connect=None,
                                               dns_answer="192.168.56.105", interval=10,
                                               dns_answer_failover=["192.168.56.22"])
        self.ping_zero_timeout = ping.Test(count=2, timeout=-4, dns_domain="test.lan", api_connect=None,
                                           dns_answer="192.168.56.105", interval=10,
                                           dns_answer_failover=["192.168.56.22"])

        self.ping_negative_interval = ping.Test(count=2, timeout=1, dns_domain="test.lan", api_connect=None, dns_answer="192.168.56.105", interval=-10, dns_answer_failover=["192.168.56.22"])
        self.ping_zero_interval = ping.Test(count=2, timeout=1, dns_domain="test.lan", api_connect=None, dns_answer="192.168.56.105", interval=0, dns_answer_failover=["192.168.56.22"])

    def test_host_up(self):
        """
        Test ping job behavior when host is up
        :return:
        """
        self.assertEqual(self.ping.job_request(host="192.168.56.105"), True)
        with self.assertLogs(level=logging.INFO) as captured_logs:
            self.ping.job_request(host="192.168.56.105")
        self.assertEqual(captured_logs.records[0].getMessage(), "Test (start) of: 192.168.56.105")
        self.assertEqual(captured_logs.records[1].getMessage(), "Test (status) of: 192.168.56.105 ok")

    def test_host_down(self):
        """
        Test ping job behavior when host is down
        :return:
        """
        self.assertEqual(self.ping.job_request(host="192.168.56.220"), False)
        with self.assertLogs(level=logging.INFO) as captured_logs:
            self.ping.job_request(host="192.168.56.220")
        self.assertEqual(captured_logs.records[0].getMessage(), "Test (start) of: 192.168.56.220")
        self.assertEqual(captured_logs.records[1].getMessage(), "Test (status) of: 192.168.56.220 host dead")

    def test_count_negative_value(self):
        """
        Test ping job behavior when count is negative
        :return:
        """
        self.assertEqual(self.ping_negative_count.job_request(host="192.168.56.105"), True)
        with self.assertLogs(level=logging.INFO) as captured_logs:
            self.ping_negative_count.job_request(host="192.168.56.105")
        self.assertEqual(captured_logs.records[0].getMessage(), "Test (start) of: 192.168.56.105")
        self.assertEqual(captured_logs.records[1].getMessage(), "Test (status) of: 192.168.56.105 ok")

    def test_zero_count(self):
        """
        Test ping job behavior when count is zero
        :return:
        """
        self.assertEqual(self.ping_zero_count.job_request(host="192.168.56.105"), True)
        with self.assertLogs(level=logging.INFO) as captured_logs:
            self.ping_zero_count.job_request(host="192.168.56.105")
        self.assertEqual(captured_logs.records[0].getMessage(), "Test (start) of: 192.168.56.105")
        self.assertEqual(captured_logs.records[1].getMessage(), "Test (status) of: 192.168.56.105 ok")

    def test_timeout_negative_value(self):
        """
        Test ping job behavior when timeout is negative
        :return:
        """
        self.assertEqual(self.ping_zero_timeout.timeout, data.PingJob.timeout)
        self.assertEqual(self.ping_negative_timeout.job_request(host="192.168.56.105"), True)
        with self.assertLogs(level=logging.INFO) as captured_logs:
            self.ping_negative_timeout.job_request(host="192.168.56.105")
        self.assertEqual(captured_logs.records[0].getMessage(), "Test (start) of: 192.168.56.105")
        self.assertEqual(captured_logs.records[1].getMessage(), "Test (status) of: 192.168.56.105 ok")

    def test_timeout_zero_value(self):
        """
        Test ping job behavior when timeout is zero
        :return:
        """
        self.assertEqual(self.ping_zero_timeout.job_request(host="192.168.56.105"), True)
        self.assertEqual(self.ping_zero_timeout.timeout, data.PingJob.timeout)
        with self.assertLogs(level=logging.INFO) as captured_logs:
            self.ping_negative_timeout.job_request(host="192.168.56.105")
        self.assertEqual(captured_logs.records[0].getMessage(), "Test (start) of: 192.168.56.105")
        self.assertEqual(captured_logs.records[1].getMessage(), "Test (status) of: 192.168.56.105 ok")

    def test_interval_negative(self):
        self.assertEqual(self.ping_negative_interval.interval, data.PingJob.interval)

    def test_interval_zero(self):
        self.assertEqual(self.ping_zero_interval.interval, data.PingJob.interval)


class TestHttp(unittest.TestCase):

    def setUp(self):
        self.http = http.Test(correct_status_code=200, interval=60, port=80, proto="http", timeout=1, dns_domain="test.lan", api_connect=None,
                            dns_answer="192.168.56.105", dns_answer_failover=["192.168.56.22"])

        self.http_wrong_code = http.Test(correct_status_code=404, interval=60, port=80, proto="http", timeout=1,
                              dns_domain="test.lan", api_connect=None,
                              dns_answer="192.168.56.105", dns_answer_failover=["192.168.56.22"])

        self.http_invalid_schema = http.Test(correct_status_code=404, interval=60, port=80, proto="", timeout=1,
                                             dns_domain="test.lan", api_connect=None,
                                             dns_answer="192.168.56.105", dns_answer_failover=["192.168.56.22"])


        self.http_negative_timeout = http.Test(correct_status_code=200, interval=60, port=80, proto="http", timeout=-10,
                                               dns_domain="test.lan", api_connect=None,
                                                dns_answer="192.168.56.105", dns_answer_failover=["192.168.56.22"])

        self.http_zero_timeout = http.Test(correct_status_code=200, interval=60, port=80, proto="http", timeout=0, dns_domain="test.lan", api_connect=None,
                            dns_answer="192.168.56.105", dns_answer_failover=["192.168.56.22"])


        self.http_negative_interval = http.Test(correct_status_code=200, interval=-60, port=80, proto="http", timeout=1, dns_domain="test.lan", api_connect=None,
                            dns_answer="192.168.56.105", dns_answer_failover=["192.168.56.22"])

        self.http_zero_interval = http.Test(correct_status_code=200, interval=0, port=80, proto="http", timeout=1, dns_domain="test.lan", api_connect=None,
                            dns_answer="192.168.56.105", dns_answer_failover=["192.168.56.22"])

    def test_host_down(self):
        self.assertEqual(self.http.job_request(host="192.168.56.222"), False)
        with self.assertLogs(level=logging.INFO) as captured_logs:
            self.http.job_request(host="192.168.56.222")
        self.assertEqual(captured_logs.records[0].getMessage(), "Test (start) of: http://192.168.56.222:80")
        self.assertEqual(captured_logs.records[1].getMessage(), "Test (status) of: http://192.168.56.222:80 failed (Connection error)")

    def test_host_up(self):
        self.assertEqual(self.http.job_request(host="192.168.56.105"), True)
        with self.assertLogs(level=logging.INFO) as captured_logs:
            self.http.job_request(host="192.168.56.105")
        self.assertEqual(captured_logs.records[0].getMessage(), "Test (start) of: http://192.168.56.105:80")
        self.assertEqual(captured_logs.records[1].getMessage(), "Test (status) of: http://192.168.56.105:80 ok")

    def test_host_up_returned_other_status_code(self):
        self.assertEqual(self.http_wrong_code.job_request(host="192.168.56.105"), False)
        with self.assertLogs(level=logging.INFO) as captured_logs:
            self.http_wrong_code.job_request(host="192.168.56.105")
        self.assertEqual(captured_logs.records[0].getMessage(), "Test (start) of: http://192.168.56.105:80")
        self.assertEqual(captured_logs.records[1].getMessage(), "Test (status) of: http://192.168.56.105:80 failed (status code 200)")

    def test_invalid_schema(self):
        self.assertEqual(self.http_invalid_schema.job_request(host="192.168.56.105"), False)
        with self.assertLogs(level=logging.INFO) as captured_logs:
            self.http_invalid_schema.job_request(host="192.168.56.105")
        self.assertEqual(captured_logs.records[0].getMessage(), "Test (start) of: 192.168.56.105:80")
        self.assertEqual(captured_logs.records[1].getMessage(), "Test (status) of: 192.168.56.105:80 failed (Invalid schema)")

    def test_interval_zero(self):
        self.assertEqual(self.http_zero_interval.interval, data.HttpJob.interval)

    def test_interval_negative(self):
        self.assertEqual(self.http_negative_interval.interval, data.HttpJob.interval)

    def test_timeout_negative(self):
        self.assertEqual(self.http_negative_timeout.job_request(host="192.168.56.105"), True)
        self.assertEqual(self.http_negative_timeout.timeout, data.HttpJob.timeout)
        with self.assertLogs(level=logging.INFO) as captured_logs:
            self.http_negative_timeout.job_request(host="192.168.56.105")
        self.assertEqual(captured_logs.records[0].getMessage(), "Test (start) of: http://192.168.56.105:80")
        self.assertEqual(captured_logs.records[1].getMessage(), "Test (status) of: http://192.168.56.105:80 ok")

    def test_timeout_zero(self):
        self.assertEqual(self.http_zero_timeout.job_request(host="192.168.56.105"), True)
        self.assertEqual(self.http_zero_timeout.timeout, data.HttpJob.timeout)
        with self.assertLogs(level=logging.INFO) as captured_logs:
            self.http_zero_timeout.job_request(host="192.168.56.105")
        self.assertEqual(captured_logs.records[0].getMessage(), "Test (start) of: http://192.168.56.105:80")
        self.assertEqual(captured_logs.records[1].getMessage(), "Test (status) of: http://192.168.56.105:80 ok")


class TestStaticEntry(unittest.TestCase):
    def setUp(self):
        self.static_entry_negative_interval = static_entry.Test(domain="test.lan", answer="1.1.1.1", interval=-10, api_connect=None)
        self.static_entry_zero_interval = static_entry.Test(domain="test.lan", answer="1.1.1.1", interval=-10, api_connect=None)

    def test_zero_interval(self):
        self.assertEqual(self.static_entry_zero_interval.interval, data.StaticEntry.interval)

    def test_negative_interval(self):
        self.assertEqual(self.static_entry_zero_interval.interval, data.StaticEntry.interval)


if __name__ == "__main__":
    unittest.main()
