"""
Configure and run jobs, interact with adguardhome

Job is a single test to perform on host for ex: get status code of a webpage or ping.
Job request is a single test performed at specific time to check host status,
for example there is a job configured to test host performed every minute,
so every minute program will start job request.
Difference between job and job request:
    Job is more like description what program must do to test a host
    Job request is a more like actual work done every x seconds to test a host

When a job request failed (host is dead), appropriate action will be done, to change dns answer of specific domain.
"""
import logging

from app.jobs import http, ping, static_entry
from app.api.connector import ApiConnector


class TestHosts:

    def __init__(self, http_configs: dict, ping_configs: dict, static_entry_configs: dict, config_configs: dict,
                 api_connector: ApiConnector, privileged=False):
        """
        Configure and run jobs, interact with adguardhome

        To run all job use method start()

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
        :param static_entry_configs: A dictionary containing all configuration about static_entry, syntax:
                            {
                                x: {
                                    'domain': # domain used in dns rewrite
                                    'answer': # dns answer
                                    'interval': # seconds between checks
                            }
        :param config_configs: A dictionary containing miscellaneous software options, syntax:
                            {
                                'entry_exist': str: # set what to do when domain is registered in AdGuardHome but
                                                      # answer don't match to any of answers from config file.
                                                      # Available options: KEEP - keep actual domain and add new,
                                                      # DELETE - delete existing domain
                                                      # DROP - treat job as if it didn't exist
                            }
        :param api_connector: object of ApiConnector class
        :param privileged: run test in privileged mode (some test need to be run by root user to open sockets)
        """
        self.http_configs = http_configs
        self.ping_configs = ping_configs
        self.static_entry_configs = static_entry_configs
        self.api_connector = api_connector
        self.config_configs = config_configs

        self.privileged = privileged

        self.ping_tasks = []
        self.http_tasks = []
        self.static_entry_tasks = []

    def add_task(self, domain: str):
        """
        Depends on config/invalid_answer and domain state decide if task should be added or not, when connection can't
        be established return False
        :return: True if task should be added, False if not (or connection can't be established)
        """
        state = self.api_connector.domain_exist(domain=domain)

        if state is None:
            return False

        if self.config_configs['entry_exist'] == "KEEP":
            return True

        if state:
            if self.config_configs['entry_exist'] == "DROP":
                return False
            else:
                existing_answer = self.api_connector.get_answer_of_domain(domain=domain)
                if type(existing_answer) is str:
                    # delete_entry can return None too
                    if self.api_connector.delete_entry(answer=existing_answer, domain=domain) is True:
                        return True
                    else:
                        return False
        return True

    def prepare_http_tasks(self):
        """
        Generate list of task based on provide config (self.http_configs)
        :return: List of tasks if provide configs are correct, False if configs contains an error
        """
        for i in range(0, len(self.http_configs)):
            try:
                if self.add_task(domain=self.http_configs[i]['dns_domain']):
                    self.http_tasks.append(http.Test(
                        correct_status_code=self.http_configs[i]['status_code'],
                        interval=self.http_configs[i]['interval'],
                        port=self.http_configs[i]['port'],
                        proto=self.http_configs[i]['proto'],
                        timeout=self.http_configs[i]['timeout'],
                        dns_answer=self.http_configs[i]['dns_answer'],
                        dns_domain=self.http_configs[i]['dns_domain'],
                        dns_answer_failover=self.http_configs[i]['dns_answer_failover'],
                        api_connect=self.api_connector))
            except KeyError:
                logging.error(msg="Internal error, provide http config missing key")
                return False
        return True

    def prepare_ping_tasks(self):
        """
        Generate list of task based on provide config (self.ping_configs)
        :return: False if configs contains an error, True if all tasks added successfully
        """

        for i in range(0, len(self.ping_configs)):
            try:
                if self.add_task(domain=self.ping_configs[i]['dns_domain']):
                    self.ping_tasks.append(ping.Test(
                        timeout=self.ping_configs[i]['timeout'],
                        count=self.ping_configs[i]['count'],
                        interval=self.ping_configs[i]['interval'],
                        dns_domain=self.ping_configs[i]['dns_domain'],
                        dns_answer=self.ping_configs[i]['dns_answer'],
                        dns_answer_failover=self.ping_configs[i]['dns_answer_failover'],
                        api_connect=self.api_connector,
                        privileged=self.privileged))
            except KeyError:
                logging.error(msg="Internal error, provide ping config missing key")
                return False
        return True

    def prepare_static_entry_tasks(self):
        for i in range(0, len(self.static_entry_configs)):
            try:
                if self.add_task(domain=self.static_entry_configs[i]['domain']):
                    self.static_entry_tasks.append(static_entry.Test(
                        domain=self.static_entry_configs[i]['domain'],
                        answer=self.static_entry_configs[i]['answer'],
                        interval=self.static_entry_configs[i]['interval'],
                        api_connect=self.api_connector))
            except KeyError:
                logging.error(msg="Internal error, provide data entry config missing key")
                return False
        return True

    def start(self):
        """
        Start test loops for all the tests provided in configs,
        loops are started only if configuration is provided and valid
        :return:
        """
        self.prepare_http_tasks()
        self.prepare_ping_tasks()
        self.prepare_static_entry_tasks()
        for task in self.ping_tasks:
            task.start()
        for task in self.http_tasks:
            task.start()
        for task in self.static_entry_tasks:
            task.start()
