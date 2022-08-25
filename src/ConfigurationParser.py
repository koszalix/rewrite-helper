import yaml
from yaml.loader import SafeLoader
import logging
import glob


class ConfigParser:
    """
    Read and parse config file. Run .parse() to run all parses.
    """

    def __init__(self, file):
        """
        :param file: path to config file
        """
        self.config_file = file
        self.file_content = {}
        self.http_configs = {}
        self.ping_configs = {}
        self.api_config = {}

    def find_any_yml(self):
        s = self.config_file
        directory = s[:len(s) - s[::-1].find("/")]
        potentially_configs_files = glob.glob(directory+"*.yml")
        if len(potentially_configs_files) >= 1:
            return potentially_configs_files[0]
        else:
            return False

    def read_config_file(self, filename):
        try:
            f = open(file=filename, mode="r")
            self.file_content = yaml.load(stream=f, Loader=SafeLoader)
            f.close()
            return 0
        except FileNotFoundError:
            return 1
        except PermissionError:
            return 2
        except IsADirectoryError:
            return 3

    def get_configs(self):
        """
        Try to read config file, if any error occurs program will exit
        :return:
        """
        file_status = self.read_config_file(filename=self.config_file)
        if file_status == 0:
            logging.info("Config loaded")
            return
        elif file_status == 1:
            potentially_file = self.find_any_yml()
            if potentially_file is not False:
                file_status = self.read_config_file(filename=potentially_file)
                if file_status == 0:
                    logging.info("Config loaded (" + str(potentially_file) + ")")
                    return
            else:
                logging.error("No config file found")
                exit(-1)
        else:
            if file_status == 1:
                logging.error("Can't load config file, file not found error")
            elif file_status == 2:
                logging.error("Can't load config file, permission error")
            elif file_status == 3:
                logging.error("Can't load config file, is a directory error")

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
        try:
            self.api_config['host'] = self.file_content['api']['host']
            self.api_config['proto'] = self.file_content['api']['proto']
            self.api_config['username'] = self.file_content['api']['username']
            self.api_config['passwd'] = self.file_content['api']['passwd']
            self.api_config['port'] = self.file_content['api']['port']
        except KeyError:
            logging.error("Config file error / api / KeyError")
            exit(-2)

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
