import yaml
from yaml.loader import SafeLoader
import logging
import glob
import os
import hashlib

from src.utils import safe_parse_value
from src.utils import check_linux_permissions

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
        """
        Find file with .yml extension
        :return:
        """
        s = self.config_file
        directory = s[:len(s) - s[::-1].find("/")]
        potentially_configs_files = glob.glob(directory+"*.yml")
        if len(potentially_configs_files) >= 1:
            for file in potentially_configs_files:
                stat_info = os.stat(file)
                if check_linux_permissions(permissions=oct(stat_info.st_mode)[-3:], target="444"):
                    return file

            return False
        else:
            return False

    def read_config_file(self, filename):
        """
        Read data from config file
        :param filename: file to read from
        :return: True if file read was successful, False in other cases
        """
        try:
            f = open(file=filename, mode="r")
            # using additional variables prevents from,  unclosed file when errors occurs while parsing yaml
            content_of_file = f.read()

            f.close()
            self.file_content = yaml.load(stream=content_of_file, Loader=SafeLoader)
            # no need to log this in production, it's handled by self.get_configs()
            logging.debug("Config file read successful")
            return True
        except FileNotFoundError:
            logging.info("Can't open config file " + filename + " file not found")
            return False
        except PermissionError:
            logging.info("Can't open config file " + filename + " permission error")
            return False
        except IsADirectoryError:
            logging.info("Can't open config file" + filename + " file is a directory")
            return False
        except yaml.parser.ParserError:
            logging.info("Error in config file, invalid syntax")
            return False

    def get_configs(self):
        """
        Try to read config file, if config.yml wasn't found try to find any *.yml file
        :return:
        """
        file_status = self.read_config_file(filename=self.config_file)
        if file_status is True:
            logging.info("Config loaded")
            return True
        else:
            potentially_file = self.find_any_yml()
            if potentially_file is not False:
                file_status = self.read_config_file(filename=potentially_file)

                if file_status is True:
                    logging.info("Config loaded (" + str(potentially_file) + ")")
                    return True

        return False

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
                self.http_configs[job_index]['dns_domain'] = job['domain']
                self.http_configs[job_index]['dns_answer'] = job['answers']['primary']

                if 'failover' in job['answers']:
                    if job['answers']['failover'] is None:
                        self.http_configs[job_index]['dns_answer_failover'] = []
                    else:
                        self.http_configs[job_index]['dns_answer_failover'] = job['answers']['failover']
                else:
                    self.http_configs[job_index]['dns_answer_failover'] = []

                self.http_configs[job_index]['interval'] = safe_parse_value(content=job, key='interval', default_value=60)
                self.http_configs[job_index]['status_code'] = safe_parse_value(content=job, key='status', default_value=200)
                self.http_configs[job_index]['proto'] = safe_parse_value(content=job, key='proto', default_value='http')
                self.http_configs[job_index]['port'] = safe_parse_value(content=job, key='port', default_value=80)

                logging.debug(msg="http-domain " + self.http_configs[job_index]['dns_domain'])
                logging.debug(msg="http-interval " + str(self.http_configs[job_index]['interval']))
                logging.debug(msg="http-status " + str(self.http_configs[job_index]['status_code']))
                logging.debug(msg="http-proto " + self.http_configs[job_index]['proto'])
                logging.debug(msg="http-port " + str(self.http_configs[job_index]['port']))
                logging.debug(msg="http-primary " + self.http_configs[job_index]['dns_answer'])
                logging.debug(msg="http-failover " + ' '.join(self.http_configs[job_index]['dns_answer_failover']))

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
                self.ping_configs[job_index]['dns_domain'] = job['domain']
                self.ping_configs[job_index]['dns_answer'] = job['answers']['primary']

                if 'failover' in job['answers']:
                    if job['answers']['failover'] is None:
                        self.ping_configs[job_index]['dns_answer_failover'] = []
                    else:
                        self.ping_configs[job_index]['dns_answer_failover'] = job['answers']['failover']
                else:
                    self.ping_configs[job_index]['dns_answer_failover'] = []

                self.ping_configs[job_index]['interval'] = safe_parse_value(content=job, key='interval', default_value=60)
                self.ping_configs[job_index]['timeout'] = safe_parse_value(content=job, key='timeout', default_value=2)
                self.ping_configs[job_index]['count'] = safe_parse_value(content=job, key='count', default_value=2)

                logging.debug(msg="ping-domain " + self.ping_configs[job_index]['dns_domain'])
                logging.debug(msg="ping-interval " + str(self.ping_configs[job_index]['interval']))
                logging.debug(msg="ping-count " + str(self.ping_configs[job_index]['count']))
                logging.debug(msg="ping-timeout " + str(self.ping_configs[job_index]['timeout']))
                logging.debug(msg="ping-primary " + self.ping_configs[job_index]['dns_answer'])
                logging.debug(msg="ping-failover " + ' '.join(self.ping_configs[job_index]['dns_answer_failover']))

                job_index = job_index + 1
            except KeyError:
                logging.error("Error in config file, ping_jobs KeyError" )

    def parse_api(self):
        """
        Parse api configuration
        :return:
        """
        try:
            self.api_config['host'] = self.file_content['api']['host']
            self.api_config['username'] = self.file_content['api']['username']
            self.api_config['passwd'] = self.file_content['api']['passwd']

            self.api_config['proto'] = safe_parse_value(content=self.file_content['api'], key='proto', default_value='http')
            self.api_config['port'] = safe_parse_value(content=self.file_content['api'], key='port', default_value=80)

            logging.debug(msg="api-host " + self.api_config['host'])
            logging.debug(msg="api-username " + self.api_config['username'])
            logging.debug(msg='api-passwd ' + hashlib.sha256(str(self.api_config['passwd']).encode()).hexdigest())
            logging.debug(msg='api-proto ' + self.api_config['proto'])
            logging.debug(msg='api-port ' + str(self.api_config['port']))

        except KeyError:
            logging.error("Config file error / api / KeyError")
            exit(-2)

    def parse(self):
        """
        Read file and parse all kind of jobs
        :return:
        """
        logging.info("Loading config")
        read_status = self.get_configs()

        if read_status is False:
            logging.error("Can't load config file")
            exit(-1)

        if "http_jobs" in self.file_content:
            logging.info(msg="http jobs found")
            self.parse_http()

        if "ping_jobs" in self.file_content:
            logging.info(msg="ping jobs found")
            self.parse_ping()

        self.parse_api()
        logging.info("Config loaded")
