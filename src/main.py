#!/bin/python3

from ApiConnector import ApiConnector
from TestHosts import TestHosts
from ConfigurationParser import ConfigParser

import asyncio
import sys


def check_args(args):
    if len(args) != 2:
        print("DNS Rewrite helper")
        print("Usage:", args[0], "<config file>")
        exit(0)


if __name__ == '__main__':
    check_args(sys.argv)

    ConfigParser = ConfigParser(sys.argv[1])
    ConfigParser.parse()

    ApiConnector = ApiConnector(config=ConfigParser.api_config)
    TestHosts = TestHosts(api_connector=ApiConnector,
                          http_configs=ConfigParser.http_configs,
                          ping_configs=ConfigParser.ping_configs)

    event_loop = asyncio.new_event_loop()
    event_loop.create_task(TestHosts.start(event_loop))

    event_loop.run_forever()
