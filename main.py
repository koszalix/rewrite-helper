#!/bin/python3
import sys
import time
import logging

from app.api.connector import ApiConnector
from app.run_jobs import TestHosts
from app.parsers.configuration import ConfigParser
from app.parsers.cli import CliParser
from app.data.config import Config as ConfigStorageConfig
from app.data.jobs_configurations import JobsConfs as ConfigStorageJobs
from app.data.api_configuration import ApiConfiguration as ConfigStorageApi


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

    ConfigStorageConfig = ConfigStorageConfig()
    ConfigStorageJobs = ConfigStorageJobs()
    ConfigStorageApi = ConfigStorageApi()

    CliParser = CliParser(sys.argv)
    CliParser.find_args()

    ConfigParser = ConfigParser(file=CliParser.config_file, confs=ConfigStorageConfig, jobs_confs=ConfigStorageJobs,
                                api_confs=ConfigStorageApi)
    ConfigParser.parse()

    if ConfigStorageConfig.log_level() is not False:
        log_level = ConfigStorageConfig.log_level()
    else:
        log_level = CliParser.log_level

    if ConfigStorageConfig.log_file != "N/A":
        log_file = ConfigStorageConfig.log_file
    else:
        log_file = CliParser.log_file
    if log_file != "":
        print("l[", log_file)
        set_log_file(filename=log_file)

    logging.getLogger().setLevel(level=log_level)

    time.sleep(ConfigStorageConfig.wait())
    ApiConnector = ApiConnector(config=ConfigStorageApi)
    TestHosts = TestHosts(api_connector=ApiConnector, jobs_confs=ConfigStorageJobs, config_configs=ConfigStorageConfig)

    TestHosts.start()
