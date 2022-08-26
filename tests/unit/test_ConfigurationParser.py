import logging
import unittest
import os

from src.ConfigurationParser import ConfigParser


class TestApi(unittest.TestCase):
    def setUp(self):
        """
        Setup directory for fixtures, some changes may be needed depends on your setup
        :return:
        """
        self.working_directory = os.getcwd() + "/tests/unit/fixtures/"
       # print("Working directory" + self.working_directory)

    def test_api_all_provided(self):
        """
        Test api configuration parser with all config provided
        :return:
        """
        parser = ConfigParser(file=self.working_directory + 'config_files/api_only_all.yml')
        parser.get_configs()
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.parse_api()
        self.assertEqual(captured_logs.records[0].getMessage(), "api-host adguard.example.com")
        self.assertEqual(captured_logs.records[1].getMessage(), "api-username admin")
        self.assertEqual(captured_logs.records[2].getMessage(), "api-passwd admin")
        self.assertEqual(captured_logs.records[3].getMessage(), "api-proto https")
        self.assertEqual(captured_logs.records[4].getMessage(), "api-port 93")

    def test_api_port_default(self):
        """
        Test api configuration parser without port provided, port should be default port 80
        :return:
        """
        parser = ConfigParser(file=self.working_directory + 'config_files/api_only_no_port.yml')
        parser.get_configs()
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.parse_api()
        self.assertEqual(captured_logs.records[0].getMessage(), "api-host adguard.example.com")
        self.assertEqual(captured_logs.records[1].getMessage(), "api-username admin")
        self.assertEqual(captured_logs.records[2].getMessage(), "api-passwd admin")
        self.assertEqual(captured_logs.records[3].getMessage(), "api-proto https")
        self.assertEqual(captured_logs.records[4].getMessage(), "api-port 80")

    def test_api_proto_default(self):
        """
        Test api configuration parser without port provided, proto should be default http
        :return:
        """
        parser = ConfigParser(file=self.working_directory + 'config_files/api_only_no_proto.yml')
        parser.get_configs()
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.parse_api()
        self.assertEqual(captured_logs.records[0].getMessage(), "api-host adguard.example.com")
        self.assertEqual(captured_logs.records[1].getMessage(), "api-username admin")
        self.assertEqual(captured_logs.records[2].getMessage(), "api-passwd admin")
        self.assertEqual(captured_logs.records[3].getMessage(), "api-proto http")
        self.assertEqual(captured_logs.records[4].getMessage(), "api-port 93")

    def test_api_all_default(self):
        """
        check if all default values all loaded correctly
        :return:
        """
        parser = ConfigParser(file=self.working_directory + 'config_files/api_only_all_default.yml')
        parser.get_configs()
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.parse_api()
        self.assertEqual(captured_logs.records[0].getMessage(), "api-host adguard.example.com")
        self.assertEqual(captured_logs.records[1].getMessage(), "api-username admin")
        self.assertEqual(captured_logs.records[2].getMessage(), "api-passwd admin")
        self.assertEqual(captured_logs.records[3].getMessage(), "api-proto http")
        self.assertEqual(captured_logs.records[4].getMessage(), "api-port 80")

class TestHttpJobs(unittest.TestCase):
    def setUp(self):
        """
        Setup directory for fixtures, some changes may be needed depends on your setup
        :return:
        """
        self.working_directory = os.getcwd() + "/tests/unit/fixtures/"
    # print("Working directory" + self.working_directory)

    def test_http_job_all_provided(self):
        parser = ConfigParser(file=self.working_directory + 'config_files/http_job.yml')
        parser.get_configs()
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.parse_http()
        self.assertEqual(captured_logs.records[0].getMessage(), "http-domain test.com")
        self.assertEqual(captured_logs.records[1].getMessage(), "http-interval 30")
        self.assertEqual(captured_logs.records[2].getMessage(), "http-status 201")
        self.assertEqual(captured_logs.records[3].getMessage(), "http-proto https")
        self.assertEqual(captured_logs.records[4].getMessage(), "http-port 8080")
        self.assertEqual(captured_logs.records[5].getMessage(), "http-primary 1.1.1.1")
        self.assertEqual(captured_logs.records[6].getMessage(), "http-failover 2.2.2.2 3.3.3.3")

    def test_http_job_all_default(self):
        parser = ConfigParser(file=self.working_directory + 'config_files/http_job_default_all.yml')
        parser.get_configs()
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.parse_http()
        self.assertEqual(captured_logs.records[0].getMessage(), "http-domain test.com")
        self.assertEqual(captured_logs.records[1].getMessage(), "http-interval 60")
        self.assertEqual(captured_logs.records[2].getMessage(), "http-status 200")
        self.assertEqual(captured_logs.records[3].getMessage(), "http-proto http")
        self.assertEqual(captured_logs.records[4].getMessage(), "http-port 80")
        self.assertEqual(captured_logs.records[5].getMessage(), "http-primary 1.1.1.1")
        self.assertEqual(captured_logs.records[6].getMessage(), "http-failover 2.2.2.2 3.3.3.3")

    def test_http_job_multiple_instances(self):
        parser = ConfigParser(file=self.working_directory + 'config_files/http_job_multiple_instances.yml')
        parser.get_configs()
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.parse_http()
        self.assertEqual(captured_logs.records[0].getMessage(), "http-domain test.com")
        self.assertEqual(captured_logs.records[1].getMessage(), "http-interval 30")
        self.assertEqual(captured_logs.records[2].getMessage(), "http-status 201")
        self.assertEqual(captured_logs.records[3].getMessage(), "http-proto https")
        self.assertEqual(captured_logs.records[4].getMessage(), "http-port 8080")
        self.assertEqual(captured_logs.records[5].getMessage(), "http-primary 1.1.1.1")
        self.assertEqual(captured_logs.records[6].getMessage(), "http-failover 2.2.2.2 3.3.3.3")
        self.assertEqual(captured_logs.records[7].getMessage(), "http-domain test-x.com")
        self.assertEqual(captured_logs.records[8].getMessage(), "http-interval 32")
        self.assertEqual(captured_logs.records[9].getMessage(), "http-status 202")
        self.assertEqual(captured_logs.records[10].getMessage(), "http-proto https")
        self.assertEqual(captured_logs.records[11].getMessage(), "http-port 8082")
        self.assertEqual(captured_logs.records[12].getMessage(), "http-primary 1.1.2.1")
        self.assertEqual(captured_logs.records[13].getMessage(), "http-failover 2.23.2.2")

    def test_http_job_no_failover(self):
        parser = ConfigParser(file=self.working_directory + 'config_files/http_job_no_failover.yml')
        parser.get_configs()
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.parse_http()
        self.assertEqual(captured_logs.records[0].getMessage(), "http-domain test.com")
        self.assertEqual(captured_logs.records[1].getMessage(), "http-interval 30")
        self.assertEqual(captured_logs.records[2].getMessage(), "http-status 201")
        self.assertEqual(captured_logs.records[3].getMessage(), "http-proto https")
        self.assertEqual(captured_logs.records[4].getMessage(), "http-port 8080")
        self.assertEqual(captured_logs.records[5].getMessage(), "http-primary 1.1.1.1")
        self.assertEqual(captured_logs.records[6].getMessage(), "http-failover ")

    def test_http_job_no_failover_2(self):
        parser = ConfigParser(file=self.working_directory + 'config_files/http_job_no_failover-2.yml')
        parser.get_configs()
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.parse_http()
        self.assertEqual(captured_logs.records[0].getMessage(), "http-domain test.com")
        self.assertEqual(captured_logs.records[1].getMessage(), "http-interval 30")
        self.assertEqual(captured_logs.records[2].getMessage(), "http-status 201")
        self.assertEqual(captured_logs.records[3].getMessage(), "http-proto https")
        self.assertEqual(captured_logs.records[4].getMessage(), "http-port 8080")
        self.assertEqual(captured_logs.records[5].getMessage(), "http-primary 1.1.1.1")
        self.assertEqual(captured_logs.records[6].getMessage(), "http-failover ")

    def test_http_job_no_failover_single(self):
        parser = ConfigParser(file=self.working_directory + 'config_files/http_job_failover-single.yml')
        parser.get_configs()
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.parse_http()
        self.assertEqual(captured_logs.records[0].getMessage(), "http-domain test.com")
        self.assertEqual(captured_logs.records[1].getMessage(), "http-interval 30")
        self.assertEqual(captured_logs.records[2].getMessage(), "http-status 201")
        self.assertEqual(captured_logs.records[3].getMessage(), "http-proto https")
        self.assertEqual(captured_logs.records[4].getMessage(), "http-port 8080")
        self.assertEqual(captured_logs.records[5].getMessage(), "http-primary 1.1.1.1")
        self.assertEqual(captured_logs.records[6].getMessage(), "http-failover 3.3.3.3")

    def test_http_job_no_interval(self):
        parser = ConfigParser(file=self.working_directory + 'config_files/http_job_no_interval.yml')
        parser.get_configs()
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.parse_http()
        self.assertEqual(captured_logs.records[0].getMessage(), "http-domain test.com")
        self.assertEqual(captured_logs.records[1].getMessage(), "http-interval 60")
        self.assertEqual(captured_logs.records[2].getMessage(), "http-status 201")
        self.assertEqual(captured_logs.records[3].getMessage(), "http-proto https")
        self.assertEqual(captured_logs.records[4].getMessage(), "http-port 8080")
        self.assertEqual(captured_logs.records[5].getMessage(), "http-primary 1.1.1.1")
        self.assertEqual(captured_logs.records[6].getMessage(), "http-failover 2.2.2.2 3.3.3.3")

    def test_http_job_no_port(self):
        parser = ConfigParser(file=self.working_directory + 'config_files/http_job_no_port.yml')
        parser.get_configs()
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.parse_http()
        self.assertEqual(captured_logs.records[0].getMessage(), "http-domain test.com")
        self.assertEqual(captured_logs.records[1].getMessage(), "http-interval 30")
        self.assertEqual(captured_logs.records[2].getMessage(), "http-status 201")
        self.assertEqual(captured_logs.records[3].getMessage(), "http-proto https")
        self.assertEqual(captured_logs.records[4].getMessage(), "http-port 80")
        self.assertEqual(captured_logs.records[5].getMessage(), "http-primary 1.1.1.1")
        self.assertEqual(captured_logs.records[6].getMessage(), "http-failover 2.2.2.2 3.3.3.3")

    def test_http_job_no_proto(self):
        parser = ConfigParser(file=self.working_directory + 'config_files/http_job_no_proto.yml')
        parser.get_configs()
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.parse_http()
        self.assertEqual(captured_logs.records[0].getMessage(), "http-domain test.com")
        self.assertEqual(captured_logs.records[1].getMessage(), "http-interval 30")
        self.assertEqual(captured_logs.records[2].getMessage(), "http-status 201")
        self.assertEqual(captured_logs.records[3].getMessage(), "http-proto http")
        self.assertEqual(captured_logs.records[4].getMessage(), "http-port 8080")
        self.assertEqual(captured_logs.records[5].getMessage(), "http-primary 1.1.1.1")
        self.assertEqual(captured_logs.records[6].getMessage(), "http-failover 2.2.2.2 3.3.3.3")

    def test_http_job_no_status(self):
        parser = ConfigParser(file=self.working_directory + 'config_files/http_job_no_status.yml')
        parser.get_configs()
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.parse_http()
        self.assertEqual(captured_logs.records[0].getMessage(), "http-domain test.com")
        self.assertEqual(captured_logs.records[1].getMessage(), "http-interval 30")
        self.assertEqual(captured_logs.records[2].getMessage(), "http-status 200")
        self.assertEqual(captured_logs.records[3].getMessage(), "http-proto https")
        self.assertEqual(captured_logs.records[4].getMessage(), "http-port 8080")
        self.assertEqual(captured_logs.records[5].getMessage(), "http-primary 1.1.1.1")
        self.assertEqual(captured_logs.records[6].getMessage(), "http-failover 2.2.2.2 3.3.3.3")


class TestPingJobs(unittest.TestCase):
    def setUp(self):
        """
        Setup directory for fixtures, some changes may be needed depends on your setup
        :return:
        """
        self.working_directory = os.getcwd() + "/tests/unit/fixtures/"
    def test_ping_job_all_provided(self):
        parser = ConfigParser(file=self.working_directory + 'config_files/ping_job.yml')
        parser.get_configs()
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.parse_ping()
        self.assertEqual(captured_logs.records[0].getMessage(), "ping-domain test.com")
        self.assertEqual(captured_logs.records[1].getMessage(), "ping-interval 44")
        self.assertEqual(captured_logs.records[2].getMessage(), "ping-count 5")
        self.assertEqual(captured_logs.records[3].getMessage(), "ping-timeout 3")
        self.assertEqual(captured_logs.records[4].getMessage(), "ping-primary 1.1.1.1")
        self.assertEqual(captured_logs.records[5].getMessage(), "ping-failover 2.2.2.2 3.3.3.3")

    def test_ping_job_all_default(self):
        parser = ConfigParser(file=self.working_directory + 'config_files/ping_job_default.yml')
        parser.get_configs()
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.parse_ping()
        self.assertEqual(captured_logs.records[0].getMessage(), "ping-domain test.com")
        self.assertEqual(captured_logs.records[1].getMessage(), "ping-interval 60")
        self.assertEqual(captured_logs.records[2].getMessage(), "ping-count 2")
        self.assertEqual(captured_logs.records[3].getMessage(), "ping-timeout 2")
        self.assertEqual(captured_logs.records[4].getMessage(), "ping-primary 1.1.1.1")
        self.assertEqual(captured_logs.records[5].getMessage(), "ping-failover 2.2.2.2 3.3.3.3")

    def test_ping_job_multiple_instances(self):
        parser = ConfigParser(file=self.working_directory + 'config_files/ping_job_multiple_instances.yml')
        parser.get_configs()
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.parse_ping()
        self.assertEqual(captured_logs.records[0].getMessage(), "ping-domain test.com")
        self.assertEqual(captured_logs.records[1].getMessage(), "ping-interval 44")
        self.assertEqual(captured_logs.records[2].getMessage(), "ping-count 5")
        self.assertEqual(captured_logs.records[3].getMessage(), "ping-timeout 3")
        self.assertEqual(captured_logs.records[4].getMessage(), "ping-primary 1.1.1.1")
        self.assertEqual(captured_logs.records[5].getMessage(), "ping-failover 2.2.2.2 3.3.3.3")
        self.assertEqual(captured_logs.records[6].getMessage(), "ping-domain test-x.com")
        self.assertEqual(captured_logs.records[7].getMessage(), "ping-interval 34")
        self.assertEqual(captured_logs.records[8].getMessage(), "ping-count 3")
        self.assertEqual(captured_logs.records[9].getMessage(), "ping-timeout 7")
        self.assertEqual(captured_logs.records[10].getMessage(), "ping-primary 1.2.1.1")
        self.assertEqual(captured_logs.records[11].getMessage(), "ping-failover 2.5.2.2 3.5.3.3")

    def test_ping_job_no_failover(self):
        parser = ConfigParser(file=self.working_directory + 'config_files/ping_job_no_failover.yml')
        parser.get_configs()
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.parse_ping()
        self.assertEqual(captured_logs.records[0].getMessage(), "ping-domain test.com")
        self.assertEqual(captured_logs.records[1].getMessage(), "ping-interval 44")
        self.assertEqual(captured_logs.records[2].getMessage(), "ping-count 5")
        self.assertEqual(captured_logs.records[3].getMessage(), "ping-timeout 3")
        self.assertEqual(captured_logs.records[4].getMessage(), "ping-primary 1.1.1.1")
        self.assertEqual(captured_logs.records[5].getMessage(), "ping-failover ")

    def test_ping_job_no_failover_2(self):
        parser = ConfigParser(file=self.working_directory + 'config_files/ping_job_no_failover-2.yml')
        parser.get_configs()
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.parse_ping()
        self.assertEqual(captured_logs.records[0].getMessage(), "ping-domain test.com")
        self.assertEqual(captured_logs.records[1].getMessage(), "ping-interval 44")
        self.assertEqual(captured_logs.records[2].getMessage(), "ping-count 5")
        self.assertEqual(captured_logs.records[3].getMessage(), "ping-timeout 3")
        self.assertEqual(captured_logs.records[4].getMessage(), "ping-primary 1.1.1.1")
        self.assertEqual(captured_logs.records[5].getMessage(), "ping-failover ")

    def test_ping_job_failover_single(self):
        parser = ConfigParser(file=self.working_directory + 'config_files/ping_job_failover-single.yml')
        parser.get_configs()
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.parse_ping()
        self.assertEqual(captured_logs.records[0].getMessage(), "ping-domain test.com")
        self.assertEqual(captured_logs.records[1].getMessage(), "ping-interval 44")
        self.assertEqual(captured_logs.records[2].getMessage(), "ping-count 5")
        self.assertEqual(captured_logs.records[3].getMessage(), "ping-timeout 3")
        self.assertEqual(captured_logs.records[4].getMessage(), "ping-primary 1.13.1.1")
        self.assertEqual(captured_logs.records[5].getMessage(), "ping-failover 2.3.2.2")

    def test_ping_job_no_interval(self):
        parser = ConfigParser(file=self.working_directory + 'config_files/ping_job_no_interval.yml')
        parser.get_configs()
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.parse_ping()
        self.assertEqual(captured_logs.records[0].getMessage(), "ping-domain test.com")
        self.assertEqual(captured_logs.records[1].getMessage(), "ping-interval 60")
        self.assertEqual(captured_logs.records[2].getMessage(), "ping-count 5")
        self.assertEqual(captured_logs.records[3].getMessage(), "ping-timeout 3")
        self.assertEqual(captured_logs.records[4].getMessage(), "ping-primary 1.1.1.1")
        self.assertEqual(captured_logs.records[5].getMessage(), "ping-failover 2.2.2.2 3.3.3.3")

    def test_ping_job_no_timeout(self):
        parser = ConfigParser(file=self.working_directory + 'config_files/ping_job_no_timeout.yml')
        parser.get_configs()
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.parse_ping()
        self.assertEqual(captured_logs.records[0].getMessage(), "ping-domain test.com")
        self.assertEqual(captured_logs.records[1].getMessage(), "ping-interval 44")
        self.assertEqual(captured_logs.records[2].getMessage(), "ping-count 5")
        self.assertEqual(captured_logs.records[3].getMessage(), "ping-timeout 2")
        self.assertEqual(captured_logs.records[4].getMessage(), "ping-primary 1.1.1.1")
        self.assertEqual(captured_logs.records[5].getMessage(), "ping-failover 2.2.2.2 3.3.3.3")

    def test_ping_job_no_count(self):
        parser = ConfigParser(file=self.working_directory + 'config_files/ping_job_no_count.yml')
        parser.get_configs()
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.parse_ping()
        self.assertEqual(captured_logs.records[0].getMessage(), "ping-domain test.com")
        self.assertEqual(captured_logs.records[1].getMessage(), "ping-interval 44")
        self.assertEqual(captured_logs.records[2].getMessage(), "ping-count 2")
        self.assertEqual(captured_logs.records[3].getMessage(), "ping-timeout 3")
        self.assertEqual(captured_logs.records[4].getMessage(), "ping-primary 1.1.1.1")
        self.assertEqual(captured_logs.records[5].getMessage(), "ping-failover 2.2.2.2 3.3.3.3")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()