import logging
import threading
import time
from typing import Union

from icmplib import NameLookupError as ICMPLookupError
from icmplib import ping

from src.api.connector import ApiConnector
from ._common import Common
from src.data import default


class Test(Common, threading.Thread):
    """
    Send ICMP package to all host mentioned in dns answers
    """

    def __init__(self, count: int, timeout: float, interval: int, dns_domain: str, dns_answer: str,
                 dns_answer_failover: list, api_connect: Union[ApiConnector, None], privileged=False):
        """
        Create configuration variables
        :param count: int: number of pakages will be sent to host
        :param timeout: int: how much test will be wait for answer from host
        :param interval: int: time between next requests in seconds
        :param dns_domain: str: domain which is used in dns rewrite
        :param dns_answer: str: default (primary) dns answers
        :param dns_answer_failover: list(str): dns answers in case when host on primary
        :param api_connect: configured ApiConnector class (on unittest set to None)
        :param privileged: run ping in privileged mode, see icmplib for documentation
         """

        # on unittest set api connect to None (avoid no necessary api object creating)
        if api_connect is not None:
            super().__init__(dns_domain=dns_domain, dns_answer=dns_answer, dns_answer_failover=dns_answer_failover,
                             api_connect=api_connect)

            threading.Thread.__init__(self)
        self.count = count

        if interval <= 0:
            self.interval = default.PingJob.interval
        else:
            self.interval = interval
        if timeout <= 0:
            self.timeout = default.PingJob.timeout
        else:
            self.timeout = timeout

        self.privileged = privileged

    def job_request(self, host: str):
        """
        Send ping to host
        :return: True if the host respond to ping, otherwise return False
        """
        try:
            logging.info("Test (start) of: " + host)
            response = ping(address=host, count=self.count, timeout=self.timeout, privileged=self.privileged)
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
            logging.info("Test start for domain:" + self.dns_domain)
            self.primary_answer_status = self.job_request(self.dns_answer_primary)
            for host_id in range(0, len(self.dns_answer_failover)):
                self.failover_answer_statuses[host_id] = self.job_request(self.dns_answer_failover[host_id])
            logging.info("Test stop for domain:" + self.dns_domain)
            self.api_callback()
            time.sleep(self.interval)
