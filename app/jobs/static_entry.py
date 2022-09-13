import logging
import threading
import time
from typing import Union

from src.api.connector import ApiConnector
from src.data import default


class Test(threading.Thread):
    def __init__(self, domain: str, answer: str, interval: int, api_connect: Union[ApiConnector, None]):
        if api_connect is not None:
            threading.Thread.__init__(self)

        self.domain = domain
        self.answer = answer
        if interval <= 0:
            self.interval = default.StaticEntry.interval
        else:
            self.interval = interval

        self.api_connect = api_connect

    def job_request(self):
        """
        Check if entry exist
        :return: True if entry exist false if not
        """
        return self.api_connect.entry_exist(answer=self.answer, domain=self.domain)

    def run(self):
        while True:
            logging.info(msg="Test start for domain:" + self.domain)
            status = self.job_request()
            if status is False:
                self.api_connect.add_entry(answer=self.answer, domain=self.domain)
            logging.info(msg="Test stop for domain:" + self.domain)
            time.sleep(self.interval)
