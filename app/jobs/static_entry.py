import logging
import threading
import time
from typing import Union

from app.api.connector import ApiConnector
from app.data.jobs_configurations import JobStaticEntry


class Test(threading.Thread):
    def __init__(self, config: JobStaticEntry, api_connect: Union[ApiConnector, None]):
        if api_connect is not None:
            threading.Thread.__init__(self)

        self.domain = config.domain()
        self.answer = config.answers()
        self.conf = config
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
            time.sleep(self.conf.interval())
