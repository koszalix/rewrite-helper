import logging
import threading

import time


import requests

from src.api.ApiConnector import ApiConnector
from ._common import Common
from src.utils import check_protocol_slashed
from src.static import data

class Test(Common, threading.Thread):
    """
    Get http(s) status code of webpage
    """

    def __init__(self, correct_status_code, interval, port, proto, dns_domain, dns_answer, timeout,
                  dns_answer_failover=None, api_connect=ApiConnector):
        """
        Create configuration variables
        :param correct_status_code: status code recognised as "host ok"
        :param interval: time between next requests in seconds
        :param port: connection port
        :param proto: connection protocol (http or https)
        :param timeout: connection timeout, if timeout is exceeded host will be treated as dead
        :param dns_domain: str: domain which is used in dns rewrite
        :param dns_answer: str: default (primary) dns answers
        :param dns_answer_failover: list(str): dns answers in case when host on primary
        :param api_connect: configured ApiConnector class
        """

        # on unittest set api connect to None (avoid no necessary api object creating)
        if api_connect is not None:
            threading.Thread.__init__(self)
            super().__init__(dns_domain=dns_domain, dns_answer=dns_answer, dns_answer_failover=dns_answer_failover,
                         api_connect=api_connect)

        self.correct_status_code = correct_status_code

        self.port = port
        self.proto = check_protocol_slashed(proto)

        if interval <= 0:
            self.interval = data.HttpJob.interval
        else:
            self.interval = interval
        if timeout <= 0:
            self.timeout = data.HttpJob.timeout
        else:
            self.timeout = timeout

    def job_request(self, host):

        """
        Test what status code website generate
        :return: True if host returns status the same code as configuration, False in other cases
        """
        try:
            logging.info("Test (start) of: " + self.proto + host + ":"+ str(self.port))
            response = requests.get(url=self.proto + host + ":" + str(self.port), timeout=self.timeout)
            if response.status_code == self.correct_status_code:
                logging.info("Test (status) of: " + self.proto + host + ":" + str(self.port) + " ok")
                return True
            else:
                logging.info(
                    "Test (status) of: " + self.proto + host + ":" + str(self.port) + " failed (status code " + str(response.status_code) + ")")
                return False
        except requests.exceptions.InvalidSchema as e:
            logging.info("Test (status) of: " + self.proto + host + ":" + str(self.port) + " failed (Invalid schema)")
            logging.warning(str(e))
            return False
        except requests.ConnectionError:
            logging.info("Test (status) of: " + self.proto + host + ":" + str(self.port) + " failed (Connection error)")
            return False

    def run(self):
        """
        Async loop for testing webpage
        :return: nothing
        """
        while True:
            logging.info("Test start for domain:" + self.dns_domain)
            self.primary_answer_status = self.job_request(self.dns_answer_primary)
            for host_id in range(0, len(self.dns_answer_failover)):
                self.failover_answer_statuses[host_id] = self.job_request(self.dns_answer_failover[host_id])
            logging.info("Test stop for domain:" + self.dns_domain)
            self.api_callback()
            time.sleep(self.interval)