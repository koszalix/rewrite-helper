#!/bin/python3
import sys
import logging
import time

from src.api.ApiConnector import ApiConnector
from src.TestHosts import TestHosts
from src.parsers.ConfigurationParser import ConfigParser
from src.parsers.CliParser import CliParser


def set_log_file(filename: str):
    log_handlers = logging.getLogger().handlers
    try:
        log_handlers[0].setStream(open(file=filename, mode='a'))
    except PermissionError:
        logging.error("Can't set log file")
    except OSError:
        logging.error("Can't set log file")


if __name__ == '__main__':
    # need to set to info to inform users about state of config file
    logging.basicConfig(level=logging.INFO)

    CliParser = CliParser(sys.argv)
    CliParser.find_args()

    ConfigParser = ConfigParser(file=CliParser.config_file)
    ConfigParser.parse()

    if ConfigParser.config_config['log_level'] is not False:
        log_level = ConfigParser.config_config['log_level']
    else:
        log_level = CliParser.log_level

    if ConfigParser.config_config['log_file'] != "N/A":
        log_file = ConfigParser.config_config['log_file']
    else:
        log_file = CliParser.log_file
    if log_file != "":
        print("l[", log_file)
        set_log_file(filename=log_file)

    logging.getLogger().setLevel(level=log_level)

    time.sleep(ConfigParser.config_config['wait'])
    ApiConnector = ApiConnector(config=ConfigParser.api_config)
    TestHosts = TestHosts(api_connector=ApiConnector,
                          http_configs=ConfigParser.http_configs,
                          ping_configs=ConfigParser.ping_configs,
                          static_entry_configs=ConfigParser.static_entry_configs,
                          config_configs=ConfigParser.config_config,
                          privileged=CliParser.run_privileged)

    TestHosts.start()
