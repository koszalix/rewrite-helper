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


from app.jobs import http, ping, static_entry
from app.api.connector import ApiConnector
from app.data.jobs_configurations import JobsConfs
from app.data.config import Config


class TestHosts:

    def __init__(self, jobs_confs: JobsConfs, config_configs: Config,
                 api_connector: ApiConnector):
        """
        Configure and run jobs, interact with adguardhome

        To run all job use method start()


        """

        self.job_confs = jobs_confs

        self.api_connector = api_connector
        self.config_configs = config_configs

        self.tasks = []

    def add_task(self, domain: str) -> bool:
        """
        Depends on config/invalid_answer and domain state decide if task should be added or not, when connection can't
        be established returns False
        :return: True if task should be added, False if not (or connection can't be established)
        """
        state = self.api_connector.domain_exist(domain=domain)

        if state is None:
            return False

        if self.config_configs.entry_exist() == "KEEP":
            return True

        if state:
            if self.config_configs.entry_exist() == "DROP":
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
        Add http jobs to task list
        :return:
        """
        for conf in self.job_confs.JobsHttp:
            if self.add_task(domain=conf.domain()):
                self.tasks.append(http.Test(config=conf, api_connect=self.api_connector))
        return True

    def prepare_ping_tasks(self):
        """"
        Add ping jobs to task list
        :return:
        """

        for conf in self.job_confs.JobsPing:
            if self.add_task(domain=conf.domain()):
                self.tasks.append(ping.Test(config=conf, api_connect=self.api_connector))
        return True

    def prepare_static_entry_tasks(self):
        """
        Add static entry jobs to task list
        :return:
        """
        for conf in self.job_confs.JobsStaticEntry:
            if self.add_task(domain=conf.domain()):
                self.tasks.append(static_entry.Test(config=conf, api_connect=self.api_connector))
        return True

    def prepare_tasks(self):
        self.prepare_http_tasks()
        self.prepare_ping_tasks()
        self.prepare_static_entry_tasks()

    def start(self):
        """
        Start test loops for all the tests provided in configs,
        loops are started only if configuration is provided and valid
        :return:
        """
        self.prepare_tasks()
        for task in self.tasks:
            task.start()
