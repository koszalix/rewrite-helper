import logging
import unittest
import os

from src.parsers.ConfigurationParser import ConfigParser


class TestInitVariable(unittest.TestCase):
    def test_init(self):
        """
        check if variables are successfully passed from arguments to class
        :return:
        """
        parser = ConfigParser("file_example")
        self.assertEqual(parser.config_file, "file_example")
        self.assertEqual(parser.file_content, {})
        self.assertEqual(parser.http_configs, {})
        self.assertEqual(parser.ping_configs, {})
        self.assertEqual(parser.api_config, {})


class TestReadConfigFile(unittest.TestCase):
    def setUp(self):
        """
        Create absolute path to config file directory
        :return:
        """
        self.working_directory = os.getcwd() + "/tests/unit/fixtures/config_files/read_config_file/"

    def test_no_permissions(self):
        """
        Test behavior of .read_config_file() when config file have invalid permissions
        :return:
        """
        parser = ConfigParser(file=self.working_directory + "no_permissions/config.yml")
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.read_config_file(filename=self.working_directory + "no_permissions/config.yml")
        self.assertEqual(captured_logs.records[0].getMessage(),
                         "Can't open config file " + self.working_directory + "no_permissions/config.yml" + " permission error")
        self.assertEqual(parser.read_config_file(filename=self.working_directory + "no_permissions/config.yml"), False)

    def test_file_no_found(self):
        """
        Test behavior of .read_config_file() when config file can not be found
        :return:
        """
        parser = ConfigParser(file=self.working_directory + "this_file_does_not_exist.yml")
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.read_config_file(filename=self.working_directory + "this_file_does_not_exist.yml")
        self.assertEqual(captured_logs.records[0].getMessage(),
                         "Can't open config file " + self.working_directory + "this_file_does_not_exist.yml" + " file not found")
        self.assertEqual(parser.read_config_file(filename=self.working_directory + "this_file_does_not_exist.yml"),
                         False)

    def test_file_is_a_directory(self):
        """
        Test behavior of .read_config_file() when config file is a directory
        :return:
        """
        parser = ConfigParser(file=self.working_directory + "a_directory")
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.read_config_file(filename=self.working_directory + "a_directory")
        self.assertEqual(captured_logs.records[0].getMessage(),
                         "Can't open config file" + self.working_directory + "a_directory" + " file is a directory")
        self.assertEqual(parser.read_config_file(filename=self.working_directory + "a_directory"), False)

    def test_correct_file(self):
        """
        Test behavior of .read_config_file() when file exist, have correct permissions and syntax
        :return:
        """
        parser = ConfigParser(file=self.working_directory + "correct_syntax.yml")
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.read_config_file(filename=self.working_directory + "correct_syntax.yml")
        self.assertEqual(captured_logs.records[0].getMessage(), "Config file read successful")
        self.assertEqual(parser.read_config_file(filename=self.working_directory + "correct_syntax.yml"), True)

    def test_invalid_file_syntax(self):
        """
        Test behavior of .read_config_file() when file exist, have correct permissions but syntax is incorrect
        :return:
        """
        parser = ConfigParser(file=self.working_directory + "incorrect_syntax.yml")
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.read_config_file(filename=self.working_directory + "incorrect_syntax.yml")
        self.assertEqual(captured_logs.records[0].getMessage(), "Error in config file, invalid syntax")
        self.assertEqual(parser.read_config_file(filename=self.working_directory + "incorrect_syntax.yml"), False)


class TestApi(unittest.TestCase):
    def setUp(self):
        """
        Create absolute path to config file directory
        :return:
        """
        self.working_directory = os.getcwd() + "/tests/unit/fixtures/config_files/api_only/"

    def test_api_all_provided(self):
        """
        Test api configuration parser with all config provided
        :return:
        """
        parser = ConfigParser(file=self.working_directory + 'api_only_all.yml')
        parser.get_configs()
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.parse_api()
        self.assertEqual(captured_logs.records[0].getMessage(), "api-host adguard.example.com")
        self.assertEqual(captured_logs.records[1].getMessage(), "api-username admin")
        self.assertEqual(captured_logs.records[2].getMessage(),
                         "api-passwd 8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918")
        self.assertEqual(captured_logs.records[3].getMessage(), "api-proto https")
        self.assertEqual(captured_logs.records[4].getMessage(), "api-port 93")

    def test_api_port_default(self):
        """
        Test api configuration parser without port provided, port should be default port 80
        :return:
        """
        parser = ConfigParser(file=self.working_directory + 'api_only_no_port.yml')
        parser.get_configs()
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.parse_api()
        self.assertEqual(captured_logs.records[0].getMessage(), "api-host adguard.example.com")
        self.assertEqual(captured_logs.records[1].getMessage(), "api-username admin")
        self.assertEqual(captured_logs.records[2].getMessage(),
                         "api-passwd 8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918")
        self.assertEqual(captured_logs.records[3].getMessage(), "api-proto https")
        self.assertEqual(captured_logs.records[4].getMessage(), "api-port 80")

    def test_api_proto_default(self):
        """
        Test api configuration parser without port provided, proto should be default http
        :return:
        """
        parser = ConfigParser(file=self.working_directory + 'api_only_no_proto.yml')
        parser.get_configs()
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.parse_api()
        self.assertEqual(captured_logs.records[0].getMessage(), "api-host adguard.example.com")
        self.assertEqual(captured_logs.records[1].getMessage(), "api-username admin")
        self.assertEqual(captured_logs.records[2].getMessage(),
                         "api-passwd 8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918")
        self.assertEqual(captured_logs.records[3].getMessage(), "api-proto http")
        self.assertEqual(captured_logs.records[4].getMessage(), "api-port 93")

    def test_api_all_default(self):
        """
        check if all default values all loaded correctly
        :return:
        """
        parser = ConfigParser(file=self.working_directory + 'api_only_all_default.yml')
        parser.get_configs()
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.parse_api()
        self.assertEqual(captured_logs.records[0].getMessage(), "api-host adguard.example.com")
        self.assertEqual(captured_logs.records[1].getMessage(), "api-username admin")
        self.assertEqual(captured_logs.records[2].getMessage(),
                         "api-passwd 8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918")
        self.assertEqual(captured_logs.records[3].getMessage(), "api-proto http")
        self.assertEqual(captured_logs.records[4].getMessage(), "api-port 80")


class TestHttpJobs(unittest.TestCase):

    def setUp(self):
        """
        Create absolute path to config file directory
        :return:
        """
        self.working_directory = os.getcwd() + "/tests/unit/fixtures/config_files/http_job/"

    def test_http_job_all_provided(self):
        """
        Test behavior of http job parser when all configuration all provided
        :return:
        """
        parser = ConfigParser(file=self.working_directory + 'http_job.yml')
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
        """
        Test behavior of http job parser when only necessary configuration options are provided
        :return:
        """
        parser = ConfigParser(file=self.working_directory + 'http_job_default_all.yml')
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
        """
        Test behavior of http job parser in case of multiple job configured
        :return:
        """
        parser = ConfigParser(file=self.working_directory + 'http_job_multiple_instances.yml')
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
        """
        Test behavior of http job parser when failover key don't exist in config file
        :return:
        """
        parser = ConfigParser(file=self.working_directory + 'http_job_no_failover.yml')
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
        """
        Test behavior of http job parser when failover key is empty in config file
        :return:
        """
        parser = ConfigParser(file=self.working_directory + 'http_job_no_failover-2.yml')
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
        """
        Test behavior of http job parser when failover key contains only single value
        :return:
        """
        parser = ConfigParser(file=self.working_directory + 'http_job_failover-single.yml')
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
        """
        Test behavior of http job parser when there is no interval specified
        :return:
        """
        parser = ConfigParser(file=self.working_directory + 'http_job_no_interval.yml')
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
        """
        Test behavior of http job parser when there is no port specified
        :return:
        """
        parser = ConfigParser(file=self.working_directory + 'http_job_no_port.yml')
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
        """
        Test behavior of http job parser when there is no protocol specified
        :return:
        """
        parser = ConfigParser(file=self.working_directory + 'http_job_no_proto.yml')
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
        """
        Test behavior of http job parser when there is no status code specified
        :return:
        """
        parser = ConfigParser(file=self.working_directory + 'http_job_no_status.yml')
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
        Create absolute path to config file directory
        :return:
        """
        self.working_directory = os.getcwd() + "/tests/unit/fixtures/config_files/ping_job/"

    def test_ping_job_all_provided(self):
        """
        Test behavior of ping job parser when all configuration all provided
        :return:
        """
        parser = ConfigParser(file=self.working_directory + 'ping_job.yml')
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
        """
        Test behavior of ping job parser when only necessary configuration options are provided
        :return:
        """
        parser = ConfigParser(file=self.working_directory + 'ping_job_default.yml')
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
        """
        Test behavior of ping job parser in case of multiple job configured
        :return:
        """
        parser = ConfigParser(file=self.working_directory + 'ping_job_multiple_instances.yml')
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
        """
        Test behavior of ping job parser when failover key don't exist in config file
        :return:
        """
        parser = ConfigParser(file=self.working_directory + 'ping_job_no_failover.yml')
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
        """
        Test behavior of http job parser when failover key is empty in config file
        :return:
        """
        parser = ConfigParser(file=self.working_directory + 'ping_job_no_failover-2.yml')
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
        """
        Test behavior of ping job parser when failover key contains only single value
        :return:
        """
        parser = ConfigParser(file=self.working_directory + 'ping_job_failover-single.yml')
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
        """
        Test behavior of ping job parser when there is no interval specified
        :return:
        """
        parser = ConfigParser(file=self.working_directory + 'ping_job_no_interval.yml')
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
        """
        Test behavior of ping job parser when there is no timeout specified
        :return:
        """
        parser = ConfigParser(file=self.working_directory + 'ping_job_no_timeout.yml')
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
        """
        Test behavior of ping job parser when there is no count specified
        :return:
        """
        parser = ConfigParser(file=self.working_directory + 'ping_job_no_count.yml')
        parser.get_configs()
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.parse_ping()
        self.assertEqual(captured_logs.records[0].getMessage(), "ping-domain test.com")
        self.assertEqual(captured_logs.records[1].getMessage(), "ping-interval 44")
        self.assertEqual(captured_logs.records[2].getMessage(), "ping-count 2")
        self.assertEqual(captured_logs.records[3].getMessage(), "ping-timeout 3")
        self.assertEqual(captured_logs.records[4].getMessage(), "ping-primary 1.1.1.1")
        self.assertEqual(captured_logs.records[5].getMessage(), "ping-failover 2.2.2.2 3.3.3.3")


class TestAnyYaml(unittest.TestCase):

    def setUp(self):
        """
        Create absolute path to config file directory
        :return:
        """
        self.working_directory = os.getcwd() + "/tests/unit/fixtures/config_files/any_yaml/"

    def test_cnf(self):
        """
        Test program behavior when specified config file doesn't exist but other .yml file exist
        :return:
        """
        parser = ConfigParser(file=self.working_directory + "cnf/config.yml")
        self.assertEqual(parser.find_any_yml(), self.working_directory + "cnf/cnf.yml")

    def test_no_file(self):
        """
        Test program behavior when specified config file doesn't exist
        :return:
        """
        parser = ConfigParser(file=self.working_directory + "no_file/config.yml")
        self.assertEqual(parser.find_any_yml(), False)

    def test_capitalised(self):
        """
        Test program behavior when specified config file doesn't exist, but the same file exist with capitalized name
        :return:
        """
        parser = ConfigParser(file=self.working_directory + "capitalised/config.yml")
        self.assertEqual(parser.find_any_yml(), self.working_directory + "capitalised/Config.yml")

    def test_all_correct(self):
        """
        Test program behavior when config file exist and have valid syntax
        :return:
        """
        parser = ConfigParser(file=self.working_directory + "all_correct/config.yml")
        self.assertEqual(parser.find_any_yml(), self.working_directory + "all_correct/config.yml")

    def test_no_permission(self):
        """
        Test program behavior when config file exist, but don't have valid syntax
        :return:
        """
        parser = ConfigParser(file=self.working_directory + "no_permissions/config.yml")
        self.assertEqual(parser.find_any_yml(), False)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
