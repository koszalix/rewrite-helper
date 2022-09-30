import logging
import threading
import time
from typing import Union

import requests

from app.api.connector import ApiConnector
from ._common import Common
from app.data.jobs_configurations import JobHttp


class Test(Common, threading.Thread):
    """
    Get http(s) status code of webpage
    """

    def __init__(self, config: JobHttp, api_connect: Union[ApiConnector, None]):
        """
        Create configuration variables

        :param api_connect: configured ApiConnector class, may be set to None by unittests
        """
        if api_connect is not None:
            threading.Thread.__init__(self)
        super().__init__(domain=config.domain(), answers=config.answers(), api_connect=api_connect)

        self.conf = config

    def job_request(self, host: str):

        """
        Test what status code website generate
        :return: True if host returns status the same code as configuration, False in other cases
        """
        try:
            logging.info("Test (start) of: " + self.conf.proto() + host + ":" + str(self.conf.port()))
            response = requests.get(url=self.conf.proto() + host + ":" + str(self.conf.port()), timeout=self.conf.timeout())
            if response.status_code == self.conf.status_code():
                logging.info("Test (status) of: " + self.conf.proto() + host + ":" + str(self.conf.port()) + " ok")
                return True
            else:
                logging.info(
                    "Test (status) of: " + self.conf.proto() + host + ":" + str(self.conf.port()) + " failed (status code " + str(
                        response.status_code) + ")")
                return False
        except requests.exceptions.InvalidSchema as e:
            logging.info("Test (status) of: " + self.conf.proto() + host + ":" + str(self.conf.port()) + " failed (Invalid schema)")
            logging.warning(str(e))
            return False
        except requests.ConnectionError:
            logging.info("Test (status) of: " + self.conf.proto() + host + ":" + str(self.conf.port()) + " failed (Connection error)")
            return False

    def run(self):
        """
        Async loop for testing webpage
        :return: nothing
        """
        while True:
            logging.info("Test start for domain:" + self.conf.domain())
            self.hosts_statuses = [self.job_request(host=host) for host in self.conf.answers()]
            logging.info("Test stop for domain:" + self.conf.domain())
            self.api_callback()
            time.sleep(self.conf.interval())
