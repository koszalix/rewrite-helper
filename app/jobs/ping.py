import logging
import threading
import time
from typing import Union

from icmplib import NameLookupError as ICMPLookupError
from icmplib import ping

from app.api.connector import ApiConnector
from ._common import Common
from app.data import default
from app.data.jobs_configurations import JobPing


class Test(Common, threading.Thread):
    """
    Send ICMP package to all host mentioned in dns answers
    """

    def __init__(self, config: JobPing, api_connect: Union[ApiConnector, None]):
        """
        Create configuration variables

        :param config: Configuration storage class for ping job
        :param api_connect: configured ApiConnector clas, may be set to None by unittests
         """
        if api_connect is not None:
            threading.Thread.__init__(self)
        super().__init__(domain=config.domain(), answers=config.answers(), api_connect=api_connect)

        self.conf = config

    def job_request(self, host: str):
        """
        Send ping to host
        :return: True if the host respond to ping, otherwise return False
        """
        try:
            logging.info("Test (start) of: " + host)
            response = ping(address=host, count=self.conf.count(), timeout=self.conf.timeout(),
                            privileged=self.conf.privileged())
            if response.is_alive:
                logging.info("Test (status) of: " + host + " ok")
            else:
                logging.info("Test (status) of: " + host + " host dead")
            return response.is_alive
        except ICMPLookupError:
            logging.info("Test (status) of: " + host + " failed ( NameLookupError )")
            return False

    def run(self):

        while True:
            logging.info("Test start for domain:" + self.conf.domain())
            self.hosts_statuses = [self.job_request(host=host) for host in self.conf.answers()]
            logging.info("Test stop for domain:" + self.conf.domain())
            self.api_callback()
            time.sleep(self.conf.interval())
