#!/bin/python3

from src.api.ApiConnector import ApiConnector
from src.TestHosts import TestHosts
from src.parsers.ConfigurationParser import ConfigParser
from src.parsers.CliParser import CliParser

import sys
import logging

if __name__ == '__main__':
    CliParser = CliParser(sys.argv)
    CliParser.find_args()

    if CliParser.log_file == "":
        logging.basicConfig(level=CliParser.log_level)
    else:
        logging.basicConfig(level=CliParser.log_level, filename=CliParser.log_file)

    ConfigParser = ConfigParser(file=CliParser.config_file)
    ConfigParser.parse()

    ApiConnector = ApiConnector(config=ConfigParser.api_config)
    TestHosts = TestHosts(api_connector=ApiConnector,
                          http_configs=ConfigParser.http_configs,
                          ping_configs=ConfigParser.ping_configs,
                          privileged=CliParser.run_privileged)

    TestHosts.start()

