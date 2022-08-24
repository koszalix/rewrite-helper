#!/bin/python3

from ApiConnector import ApiConnector
from TestHosts import TestHosts
from ConfigurationParser import ConfigParser
from CliParser import CliParser

import asyncio
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

    event_loop = asyncio.new_event_loop()
    event_loop.create_task(TestHosts.start(event_loop))

    event_loop.run_forever()
