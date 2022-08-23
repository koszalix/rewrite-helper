import asyncio
import logging

import requests

from ApiConnector import ApiConnector
from jobs._common import Common
from utils import check_protocol_slashed


class Test(Common):
    """
    Get http(s) status code of webpage
    """

    def __init__(self, correct_status_code=200, interval=60, asyncio_loop=None, proto="http://", dns_domain="",
                 dns_answer="", dns_answer_failover=None, api_connect=ApiConnector):
        """
        Create configuration variables
        :param correct_status_code: status code recognised as "host ok"
        :param interval: time between next requests in seconds
        :param asyncio_loop: asyncio event loop
        :param proto: connection protocol (http or https)
        :param dns_domain: str: domain which is used in dns rewrite
        :param dns_answer: str: default (primary) dns answers
        :param dns_answer_failover: list(str): dns answers in case when host on primary
        :param api_connect: configured ApiConnector class
        """

        super().__init__(dns_domain=dns_domain, dns_answer=dns_answer, dns_answer_failover=dns_answer_failover,
                         api_connect=api_connect)

        self.correct_status_code = correct_status_code
        self.interval = interval
        self.proto = check_protocol_slashed(proto)

        self.asyncio_loop = asyncio_loop

    def job_request(self, host):

        """
        Test what status code website generate
        :return: True if host returns status the same code as configuration, False in other cases
        """
        try:
            logging.info("Test (start) of: " + host)
            response = requests.get(self.proto + host)
            if response.status_code == self.correct_status_code:
                logging.info("Test (status) of: " + host + " ok")
                return True
            else:
                logging.info(
                    "Test (status) of: " + host + " failed (status code" + str(response.status_code) + " )")
                return False
        except requests.exceptions.MissingSchema as e:
            logging.info("Test (status) of: " + host + " failed ")
            logging.warning(str(e))
            return False
        except requests.ConnectionError:
            logging.info("Test (status) of: " + host + " failed ( Connection error )")
            return False

    async def job_loop(self):
        """
        Async loop for testing webpage
        :return: nothing
        """
        while True:
            self.primary_answer_status = self.job_request(self.dns_answer_primary)
            for host_id in range(0, len(self.dns_answer_failover)):
                self.failover_answer_statuses[host_id] = self.job_request(self.dns_answer_failover[host_id])
            self.asyncio_loop.call_soon(callback=self.callback)
            await asyncio.sleep(self.interval)


logging.basicConfig(level=logging.INFO)
