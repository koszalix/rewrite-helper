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

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()