import logging
import unittest
import os

from app.parsers.configuration import ConfigParser
from app.data.jobs_configurations import JobsConfs
from app.data.api_configuration import ApiConfiguration
from app.data.config import Config


class TestReadConfigFile(unittest.TestCase):
    def setUp(self):
        """
        Create absolute path to config file directory
        :return:
        """
        self.working_directory = os.getcwd() + "/tests/unit/fixtures/config_files/read_config_file/"
        self.c_jobs = JobsConfs()
        self.c_api = ApiConfiguration()
        self.c_conf = Config()

    def test_no_permissions(self):
        """
        Test behavior of .read_config_file() when config file have invalid permissions
        :return:
        """
        parser = ConfigParser(file=self.working_directory + "no_permissions/config.yml", jobs_confs=self.c_jobs,
                              api_confs=self.c_api, confs=self.c_conf)
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.read_config_file(filename=self.working_directory + "no_permissions/config.yml")
        self.assertEqual(captured_logs.records[0].getMessage(),
                         f"Can't open config file {self.working_directory}no_permissions/config.yml")
        self.assertEqual(parser.read_config_file(filename=self.working_directory + "no_permissions/config.yml"), False)

    def test_file_no_found(self):
        """
        Test behavior of .read_config_file() when config file can not be found
        :return:
        """
        parser = ConfigParser(file=self.working_directory + "this_file_does_not_exist.yml", jobs_confs=self.c_jobs,
                              api_confs=self.c_api, confs=self.c_conf)
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.read_config_file(filename=self.working_directory + "this_file_does_not_exist.yml")
        self.assertEqual(captured_logs.records[0].getMessage(),
                         f"Can't open config file {self.working_directory}this_file_does_not_exist.yml")
        self.assertEqual(parser.read_config_file(filename=self.working_directory + "this_file_does_not_exist.yml"),
                         False)

    def test_file_is_a_directory(self):
        """
        Test behavior of .read_config_file() when config file is a directory
        :return:
        """
        parser = ConfigParser(file=self.working_directory + "a_directory", jobs_confs=self.c_jobs,
                              api_confs=self.c_api, confs=self.c_conf)
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.read_config_file(filename=self.working_directory + "a_directory")
        self.assertEqual(captured_logs.records[0].getMessage(),
                         f"Can't open config file {self.working_directory}a_directory")
        self.assertEqual(parser.read_config_file(filename=self.working_directory + "a_directory"), False)

    def test_correct_file(self):
        """
        Test behavior of .read_config_file() when file exist, have correct permissions and syntax
        :return:
        """
        parser = ConfigParser(file=self.working_directory + "correct_syntax.yml", jobs_confs=self.c_jobs,
                              api_confs=self.c_api, confs=self.c_conf)
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.read_config_file(filename=self.working_directory + "correct_syntax.yml")
        self.assertEqual(captured_logs.records[0].getMessage(), "Config file read successful")
        self.assertEqual(parser.read_config_file(filename=self.working_directory + "correct_syntax.yml"), True)

    def test_invalid_file_syntax(self):
        """
        Test behavior of .read_config_file() when file exist, have correct permissions but syntax is incorrect
        :return:
        """
        parser = ConfigParser(file=self.working_directory + "incorrect_syntax.yml", jobs_confs=self.c_jobs,
                              api_confs=self.c_api, confs=self.c_conf)
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
        self.c_jobs = JobsConfs()

        self.c_conf = Config()

    def test_api_all_provided(self):
        """
        Test api configuration parser with all config provided
        :return:
        """
        c_api = ApiConfiguration()
        parser = ConfigParser(file=self.working_directory + 'api_only_all.yml', jobs_confs=self.c_jobs,
                              api_confs=c_api, confs=self.c_conf)
        parser.get_configs()

        parser.parse_api()

        self.assertEqual(c_api.host(), "adguard.example.com")
        self.assertEqual(c_api.username(), "admin")
        self.assertEqual(c_api.passwd(), "12345678")
        self.assertEqual(c_api.proto(), "https")
        self.assertEqual(c_api.port(), 93)
        self.assertEqual(c_api.timeout(), 7)
        self.assertEqual(c_api.startup_enable(), False)

    def test_api_port_default(self):
        """
        Test api configuration parser without port provided, port should be default port 80
        :return:
        """
        c_api = ApiConfiguration()
        parser = ConfigParser(file=self.working_directory + 'api_only_no_port.yml', jobs_confs=self.c_jobs,
                              api_confs=c_api, confs=self.c_conf)
        parser.get_configs()

        parser.parse_api()
        self.assertEqual(c_api.host(), "adguard.example.com")
        self.assertEqual(c_api.username(), "admin")
        self.assertEqual(c_api.passwd(), "12345678")
        self.assertEqual(c_api.proto(), "https")
        self.assertEqual(c_api.port(), 80)
        self.assertEqual(c_api.timeout(), 7)
        self.assertEqual(c_api.startup_enable(), False)

    def test_api_proto_default(self):
        """
        Test api configuration parser without port provided, proto should be default http
        :return:
        """
        c_api = ApiConfiguration()
        parser = ConfigParser(file=self.working_directory + 'api_only_no_proto.yml', jobs_confs=self.c_jobs,
                              api_confs=c_api, confs=self.c_conf)
        parser.get_configs()

        parser.parse_api()

        self.assertEqual(c_api.host(), "adguard.example.com")
        self.assertEqual(c_api.username(), "admin")
        self.assertEqual(c_api.passwd(), "12345678")
        self.assertEqual(c_api.proto(), "http")
        self.assertEqual(c_api.port(), 93)
        self.assertEqual(c_api.timeout(), 7)
        self.assertEqual(c_api.startup_enable(), False)

    def test_api_all_default(self):
        """
        check if all default values all loaded correctly
        :return:
        """
        c_api = ApiConfiguration()
        parser = ConfigParser(file=self.working_directory + 'api_only_all_default.yml', jobs_confs=self.c_jobs,
                              api_confs=c_api, confs=self.c_conf)
        parser.get_configs()
        parser.parse_api()

        self.assertEqual(c_api.host(), "adguard.example.com")
        self.assertEqual(c_api.username(), "admin")
        self.assertEqual(c_api.passwd(), "12345678")
        self.assertEqual(c_api.proto(), "http")
        self.assertEqual(c_api.port(), 80)
        self.assertEqual(c_api.timeout(), 10)
        self.assertEqual(c_api.startup_enable(), True)

    def test_timeout_no_provided(self):
        c_api = ApiConfiguration()
        parser = ConfigParser(file=self.working_directory + 'api_only_no_timeout.yml', jobs_confs=self.c_jobs,
                              api_confs=c_api, confs=self.c_conf)
        parser.get_configs()

        parser.parse_api()
        self.assertEqual(c_api.host(), "adguard.example.com")
        self.assertEqual(c_api.username(), "admin")
        self.assertEqual(c_api.passwd(), "12345678")
        self.assertEqual(c_api.proto(), "https")
        self.assertEqual(c_api.port(), 93)
        self.assertEqual(c_api.timeout(), 10)
        self.assertEqual(c_api.startup_enable(), False)

    def test_no_start_section(self):
        c_api = ApiConfiguration()
        parser = ConfigParser(file=self.working_directory + 'api_only_startup_empty.yml', jobs_confs=self.c_jobs,
                              api_confs=c_api, confs=self.c_conf)
        parser.get_configs()
        parser.parse_api()
        self.assertEqual(c_api.host(), "adguard.example.com")
        self.assertEqual(c_api.username(), "admin")
        self.assertEqual(c_api.passwd(), "12345678")
        self.assertEqual(c_api.proto(), "https")
        self.assertEqual(c_api.port(), 93)
        self.assertEqual(c_api.timeout(), 7)
        self.assertEqual(c_api.startup_enable(), True)


class TestHttpJobs(unittest.TestCase):

    def setUp(self):
        """
        Create absolute path to config file directory
        :return:
        """
        self.working_directory = os.getcwd() + "/tests/unit/fixtures/config_files/http_job/"
        self.c_api = ApiConfiguration()
        self.c_conf = Config()

    def test_http_job_all_provided(self):
        """
        Test behavior of http job parser when all configuration all provided
        :return:
        """
        c_jobs = JobsConfs()
        parser = ConfigParser(file=self.working_directory + 'http_job.yml', jobs_confs=c_jobs,
                              api_confs=self.c_api, confs=self.c_conf)
        parser.get_configs()

        parser.parse_http()

        self.assertEqual(c_jobs.JobsHttp[0].domain(), "test.com")
        self.assertEqual(c_jobs.JobsHttp[0].interval(), 30)
        self.assertEqual(c_jobs.JobsHttp[0].status_code(), 201)
        self.assertEqual(c_jobs.JobsHttp[0].proto(), "https")
        self.assertEqual(c_jobs.JobsHttp[0].port(), 8080)
        self.assertEqual(c_jobs.JobsHttp[0].timeout(), 12)
        self.assertEqual(c_jobs.JobsHttp[0].answers(), ["1.1.1.1", "2.2.2.2", "3.3.3.3"])

    def test_http_job_all_default(self):
        """
        Test behavior of http job parser when only necessary configuration options are provided
        :return:
        """
        c_jobs = JobsConfs()
        parser = ConfigParser(file=self.working_directory + 'http_job_default_all.yml', jobs_confs=c_jobs,
                              api_confs=self.c_api, confs=self.c_conf)
        parser.get_configs()
        parser.parse_http()

        self.assertEqual(c_jobs.JobsHttp[0].domain(), "test.com")
        self.assertEqual(c_jobs.JobsHttp[0].interval(), 60)
        self.assertEqual(c_jobs.JobsHttp[0].status_code(), 200)
        self.assertEqual(c_jobs.JobsHttp[0].proto(), "http")
        self.assertEqual(c_jobs.JobsHttp[0].port(), 80)
        self.assertEqual(c_jobs.JobsHttp[0].timeout(), 10)
        self.assertEqual(c_jobs.JobsHttp[0].answers(), ["1.1.1.1", "2.2.2.2", "3.3.3.3"])

    def test_http_job_multiple_instances(self):
        """
        Test behavior of http job parser in case of multiple job configured
        :return:
        """
        c_jobs = JobsConfs()
        parser = ConfigParser(file=self.working_directory + 'http_job_multiple_instances.yml', jobs_confs=c_jobs,
                              api_confs=self.c_api, confs=self.c_conf)
        parser.get_configs()
        parser.parse_http()

        self.assertEqual(c_jobs.JobsHttp[0].domain(), "test.com")
        self.assertEqual(c_jobs.JobsHttp[0].interval(), 30)
        self.assertEqual(c_jobs.JobsHttp[0].status_code(), 201)
        self.assertEqual(c_jobs.JobsHttp[0].proto(), "https")
        self.assertEqual(c_jobs.JobsHttp[0].port(), 8080)
        self.assertEqual(c_jobs.JobsHttp[0].timeout(), 13)
        self.assertEqual(c_jobs.JobsHttp[0].answers(), ["1.1.1.1", "2.2.2.2", "3.3.3.3"])

        self.assertEqual(c_jobs.JobsHttp[1].domain(), "test.com")
        self.assertEqual(c_jobs.JobsHttp[1].interval(), 32)
        self.assertEqual(c_jobs.JobsHttp[1].status_code(), 202)
        self.assertEqual(c_jobs.JobsHttp[1].proto(), "https")
        self.assertEqual(c_jobs.JobsHttp[1].port(), 8082)
        self.assertEqual(c_jobs.JobsHttp[1].timeout(), 14)
        self.assertEqual(c_jobs.JobsHttp[1].answers(), ["1.1.2.1", "2.23.2.2"])

    def test_http_job_no_interval(self):
        """
        Test behavior of http job parser when there is no interval specified
        :return:
        """
        c_jobs = JobsConfs()
        parser = ConfigParser(file=self.working_directory + 'http_job_no_interval.yml', jobs_confs=c_jobs,
                              api_confs=self.c_api, confs=self.c_conf)
        parser.get_configs()

        parser.parse_http()

        self.assertEqual(c_jobs.JobsHttp[0].domain(), "test.com")
        self.assertEqual(c_jobs.JobsHttp[0].interval(), 60)
        self.assertEqual(c_jobs.JobsHttp[0].status_code(), 201)
        self.assertEqual(c_jobs.JobsHttp[0].proto(), "https")
        self.assertEqual(c_jobs.JobsHttp[0].port(), 8080)
        self.assertEqual(c_jobs.JobsHttp[0].timeout(), 12)
        self.assertEqual(c_jobs.JobsHttp[0].answers(), ["1.1.1.1", "2.2.2.2", "3.3.3.3"])

    def test_http_job_no_port(self):
        """
        Test behavior of http job parser when there is no port specified
        :return:
        """
        c_jobs = JobsConfs()
        parser = ConfigParser(file=self.working_directory + 'http_job_no_port.yml', jobs_confs=c_jobs,
                              api_confs=self.c_api, confs=self.c_conf)
        parser.get_configs()
        parser.parse_http()

        self.assertEqual(c_jobs.JobsHttp[0].domain(), "test.com")
        self.assertEqual(c_jobs.JobsHttp[0].interval(), 30)
        self.assertEqual(c_jobs.JobsHttp[0].status_code(), 201)
        self.assertEqual(c_jobs.JobsHttp[0].proto(), "https")
        self.assertEqual(c_jobs.JobsHttp[0].port(), 443)
        self.assertEqual(c_jobs.JobsHttp[0].timeout(), 12)
        self.assertEqual(c_jobs.JobsHttp[0].answers(), ["1.1.1.1", "2.2.2.2", "3.3.3.3"])

    def test_http_job_no_proto(self):
        """
        Test behavior of http job parser when there is no protocol specified
        :return:
        """
        c_jobs = JobsConfs()
        parser = ConfigParser(file=self.working_directory + 'http_job_no_proto.yml', jobs_confs=c_jobs,
                              api_confs=self.c_api, confs=self.c_conf)
        parser.get_configs()
        parser.parse_http()

        self.assertEqual(c_jobs.JobsHttp[0].domain(), "test.com")
        self.assertEqual(c_jobs.JobsHttp[0].interval(), 30)
        self.assertEqual(c_jobs.JobsHttp[0].status_code(), 201)
        self.assertEqual(c_jobs.JobsHttp[0].proto(), "http")
        self.assertEqual(c_jobs.JobsHttp[0].port(), 8080)
        self.assertEqual(c_jobs.JobsHttp[0].timeout(), 12)
        self.assertEqual(c_jobs.JobsHttp[0].answers(), ["1.1.1.1", "2.2.2.2", "3.3.3.3"])

    def test_http_job_no_status_code(self):
        """
        Test behavior of http job parser when there is no status code specified
        :return:
        """
        c_jobs = JobsConfs()
        parser = ConfigParser(file=self.working_directory + 'http_job_no_status.yml', jobs_confs=c_jobs,
                              api_confs=self.c_api, confs=self.c_conf)
        parser.get_configs()
        parser.parse_http()

        self.assertEqual(c_jobs.JobsHttp[0].domain(), "test.com")
        self.assertEqual(c_jobs.JobsHttp[0].interval(), 30)
        self.assertEqual(c_jobs.JobsHttp[0].status_code(), 200)
        self.assertEqual(c_jobs.JobsHttp[0].proto(), "https")
        self.assertEqual(c_jobs.JobsHttp[0].port(), 8080)
        self.assertEqual(c_jobs.JobsHttp[0].timeout(), 12)
        self.assertEqual(c_jobs.JobsHttp[0].answers(), ["1.1.1.1", "2.2.2.2", "3.3.3.3"])

    def test_http_job_no_timeout(self):
        c_jobs = JobsConfs()
        parser = ConfigParser(file=self.working_directory + 'http_job_no_timeout.yml', jobs_confs=c_jobs,
                              api_confs=self.c_api, confs=self.c_conf)
        parser.get_configs()
        parser.parse_http()

        self.assertEqual(c_jobs.JobsHttp[0].domain(), "test.com")
        self.assertEqual(c_jobs.JobsHttp[0].interval(), 30)
        self.assertEqual(c_jobs.JobsHttp[0].status_code(), 201)
        self.assertEqual(c_jobs.JobsHttp[0].proto(), "https")
        self.assertEqual(c_jobs.JobsHttp[0].port(), 8080)
        self.assertEqual(c_jobs.JobsHttp[0].timeout(), 10)
        self.assertEqual(c_jobs.JobsHttp[0].answers(), ["1.1.1.1", "2.2.2.2", "3.3.3.3"])

    def test_http_job_auto_port_http(self):
        c_jobs = JobsConfs()
        parser = ConfigParser(file=self.working_directory + 'http_job_auto_port_http.yml', jobs_confs=c_jobs,
                              api_confs=self.c_api, confs=self.c_conf)
        parser.get_configs()
        parser.parse_http()

        self.assertEqual(c_jobs.JobsHttp[0].domain(), "test.com")
        self.assertEqual(c_jobs.JobsHttp[0].interval(), 30)
        self.assertEqual(c_jobs.JobsHttp[0].status_code(), 201)
        self.assertEqual(c_jobs.JobsHttp[0].proto(), "http")
        self.assertEqual(c_jobs.JobsHttp[0].port(), 80)
        self.assertEqual(c_jobs.JobsHttp[0].timeout(), 12)
        self.assertEqual(c_jobs.JobsHttp[0].answers(), ["1.1.1.1", "2.2.2.2", "3.3.3.3"])

    def test_http_job_auto_port_https(self):
        c_jobs = JobsConfs()
        parser = ConfigParser(file=self.working_directory + 'http_job_auto_port_https.yml', jobs_confs=c_jobs,
                              api_confs=self.c_api, confs=self.c_conf)
        parser.get_configs()

        parser.parse_http()

        self.assertEqual(c_jobs.JobsHttp[0].domain(), "test.com")
        self.assertEqual(c_jobs.JobsHttp[0].interval(), 30)
        self.assertEqual(c_jobs.JobsHttp[0].status_code(), 201)
        self.assertEqual(c_jobs.JobsHttp[0].proto(), "https")
        self.assertEqual(c_jobs.JobsHttp[0].port(), 443)
        self.assertEqual(c_jobs.JobsHttp[0].timeout(), 12)
        self.assertEqual(c_jobs.JobsHttp[0].answers(), ["1.1.1.1", "2.2.2.2", "3.3.3.3"])

    def test_http_job_invalid_domain_answer(self):
        c_jobs = JobsConfs()
        parser = ConfigParser(file=self.working_directory + 'http_invalid_domain.yml', jobs_confs=c_jobs,
                              api_confs=self.c_api, confs=self.c_conf)
        parser.get_configs()
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.parse_http()
        self.assertEqual(captured_logs.records[0].getMessage(),
                         "Job for domain: .test.com not added, due to invalid parameters")

    def test_http_job_invalid_answer(self):
        c_jobs = JobsConfs()
        parser = ConfigParser(file=self.working_directory + 'http_invalid_answer.yml', jobs_confs=c_jobs,
                              api_confs=self.c_api, confs=self.c_conf)
        parser.get_configs()
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.parse_http()
        self.assertEqual(captured_logs.records[0].getMessage(),
                         "Job for domain: test.com not added, due to invalid parameters")


class TestPingJobs(unittest.TestCase):
    def setUp(self):
        """
        Create absolute path to config file directory
        :return:
        """
        self.working_directory = os.getcwd() + "/tests/unit/fixtures/config_files/ping_job/"
        self.c_api = ApiConfiguration()
        self.c_conf = Config()

    def test_ping_job_all_provided(self):
        """
        Test behavior of ping job parser when all configuration all provided
        :return:
        """
        c_jobs = JobsConfs()
        parser = ConfigParser(file=self.working_directory + 'ping_job.yml', jobs_confs=c_jobs,
                              api_confs=self.c_api, confs=self.c_conf)
        parser.get_configs()
        parser.parse_ping()

        self.assertEqual(c_jobs.JobsPing[0].domain(), "test.com")
        self.assertEqual(c_jobs.JobsPing[0].interval(), 44)
        self.assertEqual(c_jobs.JobsPing[0].count(), 5)
        self.assertEqual(c_jobs.JobsPing[0].timeout(), 3)
        self.assertEqual(c_jobs.JobsPing[0].answers(), ["1.1.1.1", "2.2.2.2", "3.3.3.3"])
        self.assertEqual(c_jobs.JobsPing[0].privileged(), False)

    def test_ping_job_all_default(self):
        """
        Test behavior of ping job parser when only necessary configuration options are provided
        :return:
        """
        c_jobs = JobsConfs()
        parser = ConfigParser(file=self.working_directory + 'ping_job_default.yml', jobs_confs=c_jobs,
                              api_confs=self.c_api, confs=self.c_conf)
        parser.get_configs()
        parser.parse_ping()

        self.assertEqual(c_jobs.JobsPing[0].domain(), "test.com")
        self.assertEqual(c_jobs.JobsPing[0].interval(), 60)
        self.assertEqual(c_jobs.JobsPing[0].count(), 2)
        self.assertEqual(c_jobs.JobsPing[0].timeout(), 2)
        self.assertEqual(c_jobs.JobsPing[0].answers(), ["1.1.1.1", "2.2.2.2", "3.3.3.3"])
        self.assertEqual(c_jobs.JobsPing[0].privileged(), False)

    def test_ping_job_multiple_instances(self):
        """
        Test behavior of ping job parser in case of multiple job configured
        :return:
        """
        c_jobs = JobsConfs()
        parser = ConfigParser(file=self.working_directory + 'ping_job_multiple_instances.yml', jobs_confs=c_jobs,
                              api_confs=self.c_api, confs=self.c_conf)
        parser.get_configs()
        parser.parse_ping()

        self.assertEqual(c_jobs.JobsPing[0].domain(), "test.com")
        self.assertEqual(c_jobs.JobsPing[0].interval(), 44)
        self.assertEqual(c_jobs.JobsPing[0].count(), 5)
        self.assertEqual(c_jobs.JobsPing[0].timeout(), 3)
        self.assertEqual(c_jobs.JobsPing[0].answers(), ["1.1.1.1", "2.2.2.2", "3.3.3.3"])
        self.assertEqual(c_jobs.JobsPing[0].privileged(), False)

        self.assertEqual(c_jobs.JobsPing[1].domain(), "test-x.com")
        self.assertEqual(c_jobs.JobsPing[1].interval(), 34)
        self.assertEqual(c_jobs.JobsPing[1].count(), 3)
        self.assertEqual(c_jobs.JobsPing[1].timeout(), 7)
        self.assertEqual(c_jobs.JobsPing[1].answers(), ["1.2.1.1", "2.5.2.2", "3.5.3.3"])
        self.assertEqual(c_jobs.JobsPing[1].privileged(), True)

    def test_ping_job_single_answer(self):
        """
        Test behavior of ping job parser when failover key contains only single value
        :return:
        """
        c_jobs = JobsConfs()
        parser = ConfigParser(file=self.working_directory + 'ping_job_single_answer.yml', jobs_confs=c_jobs,
                              api_confs=self.c_api, confs=self.c_conf)
        parser.get_configs()
        parser.parse_ping()

        self.assertEqual(c_jobs.JobsPing[0].domain(), "test.com")
        self.assertEqual(c_jobs.JobsPing[0].interval(), 44)
        self.assertEqual(c_jobs.JobsPing[0].count(), 5)
        self.assertEqual(c_jobs.JobsPing[0].timeout(), 3)
        self.assertEqual(c_jobs.JobsPing[0].answers(), ["1.13.1.1"])
        self.assertEqual(c_jobs.JobsPing[0].privileged(), False)

    def test_ping_job_no_interval(self):
        """
        Test behavior of ping job parser when there is no interval specified
        :return:
        """
        c_jobs = JobsConfs()
        parser = ConfigParser(file=self.working_directory + 'ping_job_no_interval.yml', jobs_confs=c_jobs,
                              api_confs=self.c_api, confs=self.c_conf)
        parser.get_configs()
        parser.parse_ping()

        self.assertEqual(c_jobs.JobsPing[0].domain(), "test.com")
        self.assertEqual(c_jobs.JobsPing[0].interval(), 60)
        self.assertEqual(c_jobs.JobsPing[0].count(), 5)
        self.assertEqual(c_jobs.JobsPing[0].timeout(), 3)
        self.assertEqual(c_jobs.JobsPing[0].answers(), ["1.1.1.1", "2.2.2.2", "3.3.3.3"])
        self.assertEqual(c_jobs.JobsPing[0].privileged(), False)

    def test_ping_job_no_timeout(self):
        """
        Test behavior of ping job parser when there is no timeout specified
        :return:
        """
        c_jobs = JobsConfs()
        parser = ConfigParser(file=self.working_directory + 'ping_job_no_timeout.yml', jobs_confs=c_jobs,
                              api_confs=self.c_api, confs=self.c_conf)
        parser.get_configs()
        parser.parse_ping()

        self.assertEqual(c_jobs.JobsPing[0].domain(), "test.com")
        self.assertEqual(c_jobs.JobsPing[0].interval(), 44)
        self.assertEqual(c_jobs.JobsPing[0].count(), 5)
        self.assertEqual(c_jobs.JobsPing[0].timeout(), 2)
        self.assertEqual(c_jobs.JobsPing[0].answers(), ["1.1.1.1", "2.2.2.2", "3.3.3.3"])
        self.assertEqual(c_jobs.JobsPing[0].privileged(), False)

    def test_ping_job_no_count(self):
        """
        Test behavior of ping job parser when there is no count specified
        :return:
        """
        c_jobs = JobsConfs()
        parser = ConfigParser(file=self.working_directory + 'ping_job_no_count.yml', jobs_confs=c_jobs,
                              api_confs=self.c_api, confs=self.c_conf)
        parser.get_configs()
        parser.parse_ping()

        self.assertEqual(c_jobs.JobsPing[0].domain(), "test.com")
        self.assertEqual(c_jobs.JobsPing[0].interval(), 44)
        self.assertEqual(c_jobs.JobsPing[0].count(), 2)
        self.assertEqual(c_jobs.JobsPing[0].timeout(), 3)
        self.assertEqual(c_jobs.JobsPing[0].answers(), ["1.1.1.1", "2.2.2.2", "3.3.3.3"])
        self.assertEqual(c_jobs.JobsPing[0].privileged(), False)

    def test_ping_job_invalid_domain_answer(self):
        c_jobs = JobsConfs()
        parser = ConfigParser(file=self.working_directory + 'ping_invalid_domain.yml', jobs_confs=c_jobs,
                              api_confs=self.c_api, confs=self.c_conf)
        parser.get_configs()
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.parse_ping()
        self.assertEqual(captured_logs.records[0].getMessage(),
                         "Job for domain: -test.com not added, due to invalid parameters")

    def test_ping_job_invalid_answer_primary(self):
        c_jobs = JobsConfs()
        parser = ConfigParser(file=self.working_directory + 'ping_invalid_answer_primary.yml', jobs_confs=c_jobs,
                              api_confs=self.c_api, confs=self.c_conf)
        parser.get_configs()
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.parse_ping()
        self.assertEqual(captured_logs.records[0].getMessage(),
                         "Job for domain: test.com not added, due to invalid parameters")

    def test_ping_job_invalid_answer_failover(self):
        c_jobs = JobsConfs()
        parser = ConfigParser(file=self.working_directory + 'ping_invalid_answer_failover.yml', jobs_confs=c_jobs,
                              api_confs=self.c_api, confs=self.c_conf)
        parser.get_configs()
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.parse_ping()
        self.assertEqual(captured_logs.records[0].getMessage(),
                         "Job for domain: test-example.com not added, due to invalid parameters")


class TestStaticEntry(unittest.TestCase):
    def setUp(self):
        """
        Create absolute path to config file directory
        :return:
        """
        self.working_directory = os.getcwd() + "/tests/unit/fixtures/config_files/static_entry/"
        self.c_api = ApiConfiguration()
        self.c_conf = Config()

    def test_static_entry(self):
        c_jobs = JobsConfs()
        parser = ConfigParser(file=self.working_directory + 'static_entry.yml', jobs_confs=c_jobs,
                              api_confs=self.c_api, confs=self.c_conf)
        parser.get_configs()
        parser.parser_static_entry()

        self.assertEqual(c_jobs.JobsStaticEntry[0].domain(), "test.lan")
        self.assertEqual(c_jobs.JobsStaticEntry[0].answers(), ["1.1.1.1"])
        self.assertEqual(c_jobs.JobsStaticEntry[0].interval(), 23)

    def test_static_entry_multiple_instances(self):
        c_jobs = JobsConfs()
        parser = ConfigParser(file=self.working_directory + 'static_entry_multiple_instances.yml', jobs_confs=c_jobs,
                              api_confs=self.c_api, confs=self.c_conf)
        parser.get_configs()
        parser.parser_static_entry()

        self.assertEqual(c_jobs.JobsStaticEntry[0].domain(), "test.lan")
        self.assertEqual(c_jobs.JobsStaticEntry[0].answers(), ["1.1.1.1"])
        self.assertEqual(c_jobs.JobsStaticEntry[0].interval(), 23)

        self.assertEqual(c_jobs.JobsStaticEntry[1].domain(), "xsv.lan")
        self.assertEqual(c_jobs.JobsStaticEntry[1].answers(), ["1.2.3.4"])
        self.assertEqual(c_jobs.JobsStaticEntry[1].interval(), 44)

    def test_static_entry_no_interval(self):
        c_jobs = JobsConfs()
        parser = ConfigParser(file=self.working_directory + 'static_entry_no_interval.yml', jobs_confs=c_jobs,
                              api_confs=self.c_api, confs=self.c_conf)

        parser.parser_static_entry()
        self.assertEqual(c_jobs.JobsStaticEntry[0].domain(), "test.lan")
        self.assertEqual(c_jobs.JobsStaticEntry[0].answers(), ["1.1.1.1"])
        self.assertEqual(c_jobs.JobsStaticEntry[0].interval(), 60)

    def test_static_entry_invalid_domain_answer(self):
        c_jobs = JobsConfs()
        parser = ConfigParser(file=self.working_directory + 'static_entry_invalid_domain.yml', jobs_confs=c_jobs,
                              api_confs=self.c_api, confs=self.c_conf)
        parser.get_configs()
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.parser_static_entry()
        self.assertEqual(captured_logs.records[0].getMessage(),
                         "Job for domain: test.com- not added, due to invalid parameters")

    def test_static_entry_invalid_answer_primary(self):
        c_jobs = JobsConfs()
        parser = ConfigParser(file=self.working_directory + 'static_entry_invalid_answer.yml', jobs_confs=c_jobs,
                              api_confs=self.c_api, confs=self.c_conf)
        parser.get_configs()
        with self.assertLogs(level=logging.DEBUG) as captured_logs:
            parser.parser_static_entry()
        self.assertEqual(captured_logs.records[0].getMessage(),
                         "Job for domain: test.com not added, due to invalid parameters")


class TestAnyYaml(unittest.TestCase):

    def setUp(self):
        """
        Create absolute path to config file directory
        :return:
        """
        self.working_directory = os.getcwd() + "/tests/unit/fixtures/config_files/any_yaml/"
        self.c_jobs = JobsConfs()
        self.c_api = ApiConfiguration()
        self.c_conf = Config()

    def test_cnf(self):
        """
        Test program behavior when specified config file doesn't exist but other .yml file exist
        :return:
        """
        parser = ConfigParser(file=self.working_directory + "cnf/config.yml", jobs_confs=self.c_jobs,
                              api_confs=self.c_api, confs=self.c_conf)
        self.assertEqual(parser.find_any_yml(), self.working_directory + "cnf/cnf.yml")

    def test_no_file(self):
        """
        Test program behavior when specified config file doesn't exist
        :return:
        """
        parser = ConfigParser(file=self.working_directory + "no_file/config.yml", jobs_confs=self.c_jobs,
                              api_confs=self.c_api, confs=self.c_conf)
        self.assertEqual(parser.find_any_yml(), False)

    def test_capitalised(self):
        """
        Test program behavior when specified config file doesn't exist, but the same file exist with capitalized name
        :return:
        """
        parser = ConfigParser(file=self.working_directory + "capitalised/config.yml", jobs_confs=self.c_jobs,
                              api_confs=self.c_api, confs=self.c_conf)
        self.assertEqual(parser.find_any_yml(), self.working_directory + "capitalised/Config.yml")

    def test_all_correct(self):
        """
        Test program behavior when config file exist and have valid syntax
        :return:
        """
        parser = ConfigParser(file=self.working_directory + "all_correct/config.yml", jobs_confs=self.c_jobs,
                              api_confs=self.c_api, confs=self.c_conf)
        self.assertEqual(parser.find_any_yml(), self.working_directory + "all_correct/config.yml")

    def test_no_permission(self):
        """
        Test program behavior when config file exist, but don't have valid syntax
        :return:
        """
        parser = ConfigParser(file=self.working_directory + "no_permissions/config.yml", jobs_confs=self.c_jobs,
                              api_confs=self.c_api, confs=self.c_conf)
        self.assertEqual(parser.find_any_yml(), False)


class TestConfig(unittest.TestCase):
    """
    Test parser_config() in different circumstances
    Note
    str(logging.DEBUG) = '10'
    str(logging.INFO) = '20'
    str(logging.WARNING) = '30'
    str(logging.ERROR) = '40'
    str(logging.CRITICAL) = '50'
    """
    def setUp(self):
        """
        Create absolute path to config file directory
        :return:
        """
        self.working_directory = os.getcwd() + "/tests/unit/fixtures/config_files/config/"
        self.c_jobs = JobsConfs()
        self.c_api = ApiConfiguration()

    def test_all_default(self):
        """
        Test behavior of method parse_config() when config file don't contain config section
        :return:
        """
        c_conf = Config()
        parser = ConfigParser(file=self.working_directory + 'all_default.yml', jobs_confs=self.c_jobs,
                              api_confs=self.c_api, confs=c_conf)
        parser.get_configs()
        parser.parse_config()

        self.assertEqual(c_conf.wait(), 0)
        self.assertEqual(c_conf.log_level(), False)
        self.assertEqual(c_conf.log_file(), "N/A")
        self.assertEqual(c_conf.entry_exist(), "KEEP")

    def test_section_name_only(self):
        """
        Test behavior of method parse_config() when config file contain empty config section, other section is needed
        ( if config file is empty program-should raise another kind of exception)
        :return:
        """
        c_conf = Config()
        parser = ConfigParser(file=self.working_directory + 'section_name_only.yml', jobs_confs=self.c_jobs,
                              api_confs=self.c_api, confs=c_conf)
        parser.get_configs()
        parser.parse_config()

        self.assertEqual(c_conf.wait(), 0)
        self.assertEqual(c_conf.log_level(), False)
        self.assertEqual(c_conf.log_file(), "N/A")
        self.assertEqual(c_conf.entry_exist(), "KEEP")

    def test_no_log_level(self):
        """
        Test behavior of method parse_config() when config file contain config section without log_level parameter
        :return:
        """
        c_conf = Config()
        parser = ConfigParser(file=self.working_directory + 'no_log_level.yml', jobs_confs=self.c_jobs,
                              api_confs=self.c_api, confs=c_conf)
        parser.get_configs()
        parser.parse_config()

        self.assertEqual(c_conf.wait(), 77)
        self.assertEqual(c_conf.log_level(), False)
        self.assertEqual(c_conf.log_file(), "/var/log/log.txt")
        self.assertEqual(c_conf.entry_exist(), "DROP")

    def test_no_log_file(self):
        """
        Test behavior of method parse_config() when config file contain config section without log_file parameter
        :return:
        """
        c_conf = Config()
        parser = ConfigParser(file=self.working_directory + 'no_log_file.yml', jobs_confs=self.c_jobs,
                              api_confs=self.c_api, confs=c_conf)
        parser.get_configs()
        parser.parse_config()

        self.assertEqual(c_conf.wait(), 77)
        self.assertEqual(c_conf.log_level(), logging.DEBUG)
        self.assertEqual(c_conf.log_file(), "N/A")
        self.assertEqual(c_conf.entry_exist(), "DROP")

    def test_no_wait(self):
        """
        Test behavior of method parse_config() when config file contain config section without wait parameter
        :return:
        """
        c_conf = Config()
        parser = ConfigParser(file=self.working_directory + 'no_wait.yml', jobs_confs=self.c_jobs,
                              api_confs=self.c_api, confs=c_conf)
        parser.get_configs()
        parser.parse_config()

        self.assertEqual(c_conf.wait(), 0)
        self.assertEqual(c_conf.log_level(), logging.DEBUG)
        self.assertEqual(c_conf.log_file(), "/var/log/log.txt")
        self.assertEqual(c_conf.entry_exist(), "DROP")

    def test_no_invalid_entry(self):
        """
        Test behavior of method parse_config() when config file contain config section without invalid_entry parameter
        :return:
        """
        c_conf = Config()
        parser = ConfigParser(file=self.working_directory + 'no_invalid_entry.yml', jobs_confs=self.c_jobs,
                              api_confs=self.c_api, confs=c_conf)
        parser.get_configs()
        parser.parse_config()

        self.assertEqual(c_conf.wait(), 77)
        self.assertEqual(c_conf.log_level(), logging.DEBUG)
        self.assertEqual(c_conf.log_file(), "/var/log/log.txt")
        self.assertEqual(c_conf.entry_exist(), "KEEP")

        
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
