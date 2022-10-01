import logging
import unittest

from app.jobs import ping, http, static_entry
from app.data.jobs_configurations import JobPing, JobHttp, JobStaticEntry


class TestException(Exception):
    """
    Exception used to end infinite loop in job, raised by dummy_api_callback
    """
    pass


def dummy_api_callback():
    """
    Function used to overwrite _common.api_callback(), when unit tests don't need to use api
    :return:
    """
    raise TestException


class TestPing(unittest.TestCase):

    def setUp(self):

        c_ping = JobPing(interval=10, count=2, timeout=0.2, domain="test.lan",
                         answers=["192.168.56.105", "192.168.56.22"], privileged=False)

        self.ping = ping.Test(config=c_ping, api_connect=None)
        self.ping.api_callback = dummy_api_callback

    # test job requests
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

    def test_host_statuses(self):
        """
        Test if host statuses are correctly added to status list
        :return:
        """
        with self.assertRaises(TestException):
            self.ping.run()
        self.assertEqual(self.ping.hosts_statuses, [True, False])


class TestHttp(unittest.TestCase):

    def setUp(self):
        c_http = JobHttp(interval=60, status_code=200, proto="http", domain="test.lan",
                         answers=["192.168.56.105", "192.168.56.22"], timeout=1, port=80)
        c_http_wrong_code = JobHttp(interval=60, status_code=404, proto="http", domain="test.lan",
                                    answers=["192.168.56.105", "192.168.56.22"], timeout=1, port=80)
        c_http_invalid_schema = JobHttp(interval=60, status_code=404, proto="", domain="test.lan",
                                        answers=["192.168.56.105", "192.168.56.22"], timeout=1, port=80)

        self.http = http.Test(config=c_http, api_connect=None)
        self.http.api_callback = dummy_api_callback

        self.http_wrong_code = http.Test(config=c_http_wrong_code, api_connect=None)
        self.http_wrong_code.api_callback = dummy_api_callback

        self.http_invalid_schema = http.Test(config=c_http_invalid_schema, api_connect=None)
        self.http_invalid_schema.api_connector = dummy_api_callback

    def test_host_down(self):
        self.assertEqual(self.http.job_request(host="192.168.56.222"), False)
        with self.assertLogs(level=logging.INFO) as captured_logs:
            self.http.job_request(host="192.168.56.222")
        self.assertEqual(captured_logs.records[0].getMessage(), "Test (start) of: http://192.168.56.222:80")
        self.assertEqual(captured_logs.records[1].getMessage(),
                         "Test (status) of: http://192.168.56.222:80 failed (Connection error)")

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
        self.assertEqual(captured_logs.records[1].getMessage(),
                         "Test (status) of: http://192.168.56.105:80 failed (status code 200)")

    def test_invalid_schema(self):
        self.assertEqual(self.http_invalid_schema.job_request(host="192.168.56.105"), False)
        with self.assertLogs(level=logging.INFO) as captured_logs:
            self.http_invalid_schema.job_request(host="192.168.56.105")
        self.assertEqual(captured_logs.records[0].getMessage(), "Test (start) of: 192.168.56.105:80")
        self.assertEqual(captured_logs.records[1].getMessage(),
                         "Test (status) of: 192.168.56.105:80 failed (Invalid schema)")

    def test_host_statuses(self):
        """
        Test if host statuses are correctly added to status list
        :return:
        """
        with self.assertRaises(TestException):
            self.http.run()
        self.assertEqual(self.http.hosts_statuses, [True, False])


class TestStaticJob(unittest.TestCase):
    # TODO: tests for static entry
    def setUp(self):
        c_static_entry = JobStaticEntry(interval=10, domain="test.lan", answer="192.168.56.105")
        self.staticEntry = static_entry.Test(config=c_static_entry, api_connect=None)


if __name__ == "__main__":
    unittest.main()
