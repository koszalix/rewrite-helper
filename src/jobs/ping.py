import asyncio
import logging

from icmplib import NameLookupError as ICMPLookupError
from icmplib import ping

from ApiConnector import ApiConnector
from jobs._common import Common


class Test(Common):
    """
    Send ICMP package to all host mentioned in dns answers
    """

    def __init__(self, count=2, timeout=4, interval=60, asyncio_loop=None, dns_domain="", dns_answer="",
                 dns_answer_failover=None, api_connect=ApiConnector):
        """
        Create configuration variables
        :param count: int: number of pakages will be sent to host
        :param timeout: int: how much test will be wait for answer from host
        :param interval: int: time between next requests in seconds
        :param dns_domain: str: domain which is used in dns rewrite
        :param dns_answer: str: default (primary) dns answers
        :param dns_answer_failover: list(str): dns answers in case when host on primary
        :param asyncio_loop: asyncio event loop
        :param api_connect: configured ApiConnector class
         """

        super().__init__(dns_domain=dns_domain, dns_answer=dns_answer, dns_answer_failover=dns_answer_failover,
                         api_connect=api_connect)

        self.timeout = timeout
        self.count = count
        self.interval = interval

        self.asyncio_loop = asyncio_loop

    def job_request(self, host):
        """
        Send ping to host
        :return: True if the host respond to ping, otherwise return False
        """
        try:
            logging.info("Test (start) of: " + host)
            response = ping(address=host, count=self.count, timeout=self.timeout)
            if response.is_alive:
                logging.info("Test (status) of: " + host + " ok")
            else:
                logging.info("Test (status) of: " + host + " host dead")
            return response.is_alive
        except ICMPLookupError:
            logging.info("Test (status) of: " + host + " failed ( NameLookupError )")
            return False

    async def job_loop(self):
        while True:

            self.primary_answer_status = self.job_request(self.dns_answer_primary)
            for host_id in range(0, len(self.dns_answer_failover)):
                self.failover_answer_statuses[host_id] = self.job_request(self.dns_answer_failover[host_id])
            self.asyncio_loop.call_soon(callback=self.callback)
            await asyncio.sleep(self.interval)


logging.basicConfig(level=logging.INFO)  # change to info
