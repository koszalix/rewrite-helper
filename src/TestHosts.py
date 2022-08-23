"""
Perform test on hosts
"""

import logging

from jobs import http, ping


class TestHosts:

    def __init__(self, http_configs=None, ping_configs=None, api_connector=None):
        """
        Configure and run jobs, interact with adguardhome
        Job is a single test to perform on host for ex: get status code of a webpage or ping.
        Job request is a single test performed at specific time to check host status,
        For example there is a job configured to test host performed every minute,
        so every minute program will start job request.
        Difference between job and job request:
            Job is more like description what program must do to test a host
            Job request is a more like actual work done every x seconds to test a host

        To run all job use method start()

        When a job request failed (host is dead), appropriate action will be done, to change dns answer of specific
        domain.

        :param http_configs:  A dictionary containing all configuration about http job, syntax:
                            {
                             x: {
                                    'interval': # seconds between job requests,
                                    'status_code': # status code recognised as "host ok",
                                    'proto': # protocol http or https
                                    'dns_domain': # domain used in dns rewrite
                                    'dns_answer: default (primary) dns name
                                    'dns_answer_failover': ['failover 1', 'failover 2'] # dns answers when primary is
                                                                                        # not working

                                },
                            }
                            x - is next decimal number, starting from zero. Each job must have their own individual
                            number.
        :param ping_configs: A dictionary containing all configuration about ping job, syntax:
                            {
                            x: {
                                 'interval': # seconds between job requests,
                                 'count': # number of packages send on each job request,
                                 'timeout': # time after which (if there is no response from host),
                                            # host will be treated as dead
                                 'dns_domain': # domain used in dns rewrite
                                 'dns_answer: default (primary) dns name
                                 'dns_answer_failover': ['failover 1', 'failover 2'] # dns answers when primary is
                                                                                     # not working
                            },
                            }
        :param api_connector: object of ApiConnector class
        """
        self.http_configs = http_configs
        self.ping_configs = ping_configs

        self.asyncio_loop = None
        self.api_connector = api_connector

    def prepare_http_tasks(self):
        """
        Generate list of task based on provide config (self.http_configs)
        :return: List of tasks if provide configs are correct, False if configs contains an error
        """
        http_tasks = []
        for i in range(0, len(self.http_configs)):
            try:
                http_tasks.append(self.asyncio_loop.create_task(http.Test(
                    correct_status_code=self.http_configs[i]['status_code'],
                    interval=self.http_configs[i]['interval'],
                    asyncio_loop=self.asyncio_loop,
                    proto=self.http_configs[i]['proto'],
                    dns_answer=self.http_configs[i]['dns_answer'],
                    dns_domain=self.http_configs[i]['dns_domain'],
                    dns_answer_failover=self.http_configs[i][
                        'dns_answer_failover'],
                    api_connect=self.api_connector).job_loop()))

            except KeyError:
                logging.error("Internal error, provide http config missing key")
                return False
        return http_tasks

    async def await_http_tasks(self):
        """
        Await http task from self.prepare_http_tasks()
        :return: nothing
        """
        tasks = self.prepare_http_tasks()
        if type(tasks) == list:
            for task in tasks:
                await task
        else:
            logging.error(msg="Can't load http configs")

    def prepare_ping_tasks(self):
        """
        Generate list of task based on provide config (self.ping_configs)
        :return: List of tasks if provide configs are correct, False if configs contains an error
        """
        ping_tasks = []
        for i in range(0, len(self.ping_configs)):
            try:
                ping_tasks.append(self.asyncio_loop.create_task(
                    ping.Test(timeout=self.ping_configs[i]['timeout'],
                              count=self.ping_configs[i]['count'],
                              interval=self.ping_configs[i]['interval'],
                              dns_domain=self.ping_configs[i]['dns_domain'],
                              dns_answer=self.ping_configs[i]['dns_answer'],
                              dns_answer_failover=self.ping_configs[i]['dns_answer_failover'],
                              asyncio_loop=self.asyncio_loop,
                              api_connect=self.api_connector).job_loop()))
            except KeyError:
                logging.error("Internal error, provide ping config missing key")
                return False
        return ping_tasks

    async def await_ping_tasks(self):
        """
        Await ping task from self.prepare_ping_tasks()
        :return: nothing
        """
        tasks = self.prepare_ping_tasks()
        if type(tasks) == list:
            for task in tasks:
                await task

        else:
            logging.error(msg="Can't load http configs")

    async def await_tasks(self):
        tasks = self.prepare_ping_tasks()
        for task in tasks:
            print(task)
            await task
        tasks = self.prepare_http_tasks()
        for task in tasks:
            await task

    async def start(self, loop=None):
        """
        Start test loops for all the tests provided in configs,
        loops are started only if configuration is provided and valid
        :return:
        """
        self.asyncio_loop = loop

        #if self.http_configs is not None:
         #   self.await_http_tasks()
          #  http_task = loop.create_task(self.await_http_tasks())
         #   await http_task
       # if self.ping_configs is not None:
        #  self.await_ping_tasks()
          #  ping_task = loop.create_task(self.await_ping_tasks())
          #  await ping_task
        await self.await_tasks()

logging.basicConfig(level=logging.INFO)