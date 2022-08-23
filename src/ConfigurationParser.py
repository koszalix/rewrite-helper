import yaml
from yaml.loader import SafeLoader
import logging


class ConfigParser:
    """
    Read and parse config file. Run .parse() to run all parses.
    """

    def __init__(self, path):
        """
        :param path: path to config file
        """
        self.config_path = path
        self.file_content = {}
        self.http_configs = {}
        self.ping_configs = {}
        self.api_config = {}

    def get_configs(self):
        """
        Try to read config file, if any error occurs program will exit
        :return:
        """
        try:
            f = open(file=self.config_path, mode="r")
            self.file_content = yaml.load(stream=f, Loader=SafeLoader)
            f.close()
        except FileNotFoundError:
            logging.error(msg="Can't read config file, file not found")
            exit(-1)

        except PermissionError:
            logging.error(msg="Can't read config file, file not found")
            exit(-1)

    def parse_http(self):
        """
        Parse http jobs, create dictionary compatible with TestHosts.py
        :return:
        """
        job_index = 0
        for jobs in self.file_content['http_jobs']:
            try:
                job = jobs['job']
                self.http_configs[job_index] = {}
                self.http_configs[job_index]['interval'] = job['interval']
                self.http_configs[job_index]['status_code'] = job['status']
                self.http_configs[job_index]['proto'] = job['proto']
                self.http_configs[job_index]['dns_domain'] = job['domain']
                self.http_configs[job_index]['dns_answer'] = job['answers']['primary']
                self.http_configs[job_index]['dns_answer_failover'] = job['answers']['failover']
                job_index = job_index + 1
            except KeyError:
                logging.error("Error in config file, http_jobs KeyError")

    def parse_ping(self):
        """
        Parse ping job, create dictionary compatible with TestHosts.py
        :return:
        """
        job_index = 0
        for jobs in self.file_content['ping_jobs']:
            try:
                job = jobs['job']
                self.ping_configs[job_index] = {}
                self.ping_configs[job_index]['interval'] = job['interval']
                self.ping_configs[job_index]['count'] = job['count']
                self.ping_configs[job_index]['timeout'] = job['timeout']
                self.ping_configs[job_index]['dns_domain'] = job['domain']
                self.ping_configs[job_index]['dns_answer'] = job['answers']['primary']
                self.ping_configs[job_index]['dns_answer_failover'] = job['answers']['failover']
                job_index = job_index + 1
            except KeyError:
                logging.error("Error in config file, ping_jobs KeyError")

    def parse_api(self):
        """
        Parse api configuration
        :return:
        """
        self.api_config['host'] = self.file_content['api']['host']
        self.api_config['proto'] = self.file_content['api']['proto']
        self.api_config['username'] = self.file_content['api']['username']
        self.api_config['passwd'] = self.file_content['api']['passwd']

    def parse(self):
        """
        Read file and parse all kind of jobs
        :return:
        """
        logging.info("Loading config")
        self.get_configs()
        if "http_jobs" in self.file_content:
            logging.info(msg="http jobs found")
            self.parse_http()

        if "ping_jobs" in self.file_content:
            logging.info(msg="ping jobs found")
            self.parse_ping()

        self.parse_api()
        logging.info("Config loaded")


logging.basicConfig(level=logging.INFO)
