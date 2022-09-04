import yaml
from yaml.loader import SafeLoader
import logging
import glob
import os
import hashlib

from src.utils import parse_value_with_default
from src.utils import check_linux_permissions
from src.utils import parse_logging_level
from src.utils import match_port_to_protocol
from src.data import default_data


class ConfigParser:
    """
    Read and parse config file. Run .parse() to run all parses.
    """

    def __init__(self, file: str):
        """
        :param file: path to config file
        """
        self.config_file = file
        self.file_content = {}
        self.http_configs = {}
        self.ping_configs = {}
        self.static_entry_configs = {}
        self.api_config = {}
        self.config_config = {}

    def find_any_yml(self):
        """
        Find file with .yml extension
        :return:
        """
        s = self.config_file
        directory = s[:len(s) - s[::-1].find("/")]
        potentially_configs_files = glob.glob(directory + "*.yml")
        if len(potentially_configs_files) >= 1:
            for file in potentially_configs_files:
                stat_info = os.stat(file)
                if check_linux_permissions(permissions=oct(stat_info.st_mode)[-3:], target="444"):
                    return file

            return False
        else:
            return False

    def read_config_file(self, filename: str):
        """
        Read data from config file
        :param filename: file to read from
        :return: True if file read was successful, False in other cases
        """
        try:
            f = open(file=filename, mode="r")
            # using additional variables prevents from unclosed file, when errors occur while parsing yaml
            content_of_file = f.read()

            f.close()
            self.file_content = yaml.load(stream=content_of_file, Loader=SafeLoader)
            if self.file_content is None:
                logging.error("Can't load config file, file empty")
                return False
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
        except yaml.YAMLError:
            logging.info("Error in config file, invalid syntax")
            return False
        except OSError:
            logging.info("Can't open config file" + filename + " OS error")

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

                self.http_configs[job_index]['interval'] = parse_value_with_default(content=job, key='interval',
                                                                                    default_value=
                                                                                    default_data.HttpJob.interval)
                self.http_configs[job_index]['status_code'] = parse_value_with_default(content=job, key='status',
                                                                                       default_value=
                                                                                       default_data.HttpJob.status)
                self.http_configs[job_index]['proto'] = parse_value_with_default(content=job, key='proto',
                                                                                 default_value='http')
                self.http_configs[job_index]['port'] = parse_value_with_default(content=job, key='port',
                                                                                default_value=match_port_to_protocol(
                                                                                    proto=self.http_configs[job_index][
                                                                                        'proto'],
                                                                                    default_port=
                                                                                    default_data.HttpJob.port)
                                                                                )

                self.http_configs[job_index]['timeout'] = parse_value_with_default(content=job, key='timeout',
                                                                                   default_value=
                                                                                   default_data.HttpJob.timeout)

                logging.debug(msg="http-domain " + self.http_configs[job_index]['dns_domain'])
                logging.debug(msg="http-interval " + str(self.http_configs[job_index]['interval']))
                logging.debug(msg="http-status " + str(self.http_configs[job_index]['status_code']))
                logging.debug(msg="http-proto " + self.http_configs[job_index]['proto'])
                logging.debug(msg="http-port " + str(self.http_configs[job_index]['port']))
                logging.debug(msg="http-primary " + self.http_configs[job_index]['dns_answer'])
                logging.debug(msg="http-failover " + ' '.join(self.http_configs[job_index]['dns_answer_failover']))
                logging.debug(msg="http-timeout " + str(self.http_configs[job_index]['timeout']))

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

                self.ping_configs[job_index]['interval'] = parse_value_with_default(content=job, key='interval',
                                                                                    default_value=
                                                                                    default_data.PingJob.interval)
                self.ping_configs[job_index]['timeout'] = parse_value_with_default(content=job, key='timeout',
                                                                                   default_value=
                                                                                   default_data.PingJob.timeout)
                self.ping_configs[job_index]['count'] = parse_value_with_default(content=job, key='count',
                                                                                 default_value=
                                                                                 default_data.PingJob.count)

                logging.debug(msg="ping-domain " + self.ping_configs[job_index]['dns_domain'])
                logging.debug(msg="ping-interval " + str(self.ping_configs[job_index]['interval']))
                logging.debug(msg="ping-count " + str(self.ping_configs[job_index]['count']))
                logging.debug(msg="ping-timeout " + str(self.ping_configs[job_index]['timeout']))
                logging.debug(msg="ping-primary " + self.ping_configs[job_index]['dns_answer'])
                logging.debug(msg="ping-failover " + ' '.join(self.ping_configs[job_index]['dns_answer_failover']))

                job_index = job_index + 1
            except KeyError:
                logging.error("Error in config file, ping_jobs KeyError")

    def parser_static_entry(self):
        job_index = 0
        for jobs in self.file_content['static_entry']:
            try:
                job = jobs['job']
                self.static_entry_configs[job_index] = {}
                self.static_entry_configs[job_index]['domain'] = job['domain']
                self.static_entry_configs[job_index]['answer'] = job['answer']
                self.static_entry_configs[job_index]['interval'] = parse_value_with_default(
                                                                                    content=job,
                                                                                    key='interval',
                                                                                    default_value=
                                                                                    default_data.StaticEntry.interval)
                logging.debug(msg="data-entry-domain " + self.static_entry_configs[job_index]['domain'])
                logging.debug(msg="data-entry-answer " + self.static_entry_configs[job_index]['answer'])
                logging.debug(msg="data-entry-interval " + str(self.static_entry_configs[job_index]['interval']))

                job_index += 1
            except KeyError:
                logging.error("Error in config file, static_entry KeyError")

    def parse_api(self):
        """
        Parse api configuration
        :return:
        """
        try:
            self.api_config['host'] = self.file_content['api']['host']
            self.api_config['username'] = self.file_content['api']['username']
            self.api_config['passwd'] = self.file_content['api']['passwd']

            self.api_config['proto'] = parse_value_with_default(content=self.file_content['api'], key='proto',
                                                                default_value=default_data.Api.proto)
            self.api_config['port'] = parse_value_with_default(content=self.file_content['api'], key='port',
                                                               default_value=default_data.Api.port)
            self.api_config['timeout'] = parse_value_with_default(content=self.file_content['api'], key='timeout',
                                                                  default_value=default_data.Api.timeout)
            if 'startup' in self.file_content['api']:
                self.api_config['startup'] = {}
                self.api_config['startup']['test'] = parse_value_with_default(
                    content=self.file_content['api']['startup'],
                    key='test', default_value=default_data.Api.Startup.test)
                self.api_config['startup']['timeout'] = parse_value_with_default(
                    content=self.file_content['api']['startup'],
                    key='timeout', default_value=default_data.Api.Startup.timeout)
                self.api_config['startup']['exit_on_fail'] = parse_value_with_default(
                    content=self.file_content['api']['startup'], key='exit_on_fail',
                    default_value=default_data.Api.Startup.exit_on_false)
                self.api_config['startup']['retry_after'] = parse_value_with_default(
                    content=self.file_content['api']['startup'], key='retry_after',
                    default_value=default_data.Api.Startup.retry_after)
            else:
                self.api_config['startup'] = {}
                self.api_config['startup']['test'] = True
                self.api_config['startup']['timeout'] = 10
                self.api_config['startup']['exit_on_fail'] = False
                self.api_config['startup']['retry_after'] = 10

            logging.debug(msg="api-host " + self.api_config['host'])
            logging.debug(msg="api-username " + self.api_config['username'])
            logging.debug(msg='api-passwd ' + hashlib.sha256(str(self.api_config['passwd']).encode()).hexdigest())
            logging.debug(msg='api-proto ' + self.api_config['proto'])
            logging.debug(msg='api-port ' + str(self.api_config['port']))
            logging.debug(msg='api-timeout ' + str(self.api_config['timeout']))
            logging.debug(msg='api-startup-test ' + str(self.api_config['startup']['test']))
            logging.debug(msg='api-startup-timeout ' + str(self.api_config['startup']['timeout']))
            logging.debug(msg='api-startup-exit_on_fail ' + str(self.api_config['startup']['exit_on_fail']))
            logging.debug(msg='api-startup-test-retry_after ' + str(self.api_config['startup']['retry_after']))

        except KeyError:
            logging.error("Config file error / api / KeyError")
            exit(-2)

    def parse_config(self):
        """
        Pase config section
        :return:
        """
        try:
            if 'config' in self.file_content:
                self.config_config['wait'] = parse_value_with_default(
                    content=self.file_content['config'], key='wait', default_value=default_data.Config.wait)
                log_level = parse_value_with_default(
                    content=self.file_content['config'], key="log_level", default_value="N/A")

                self.config_config['log_level'] = parse_logging_level(logging_str=log_level)

                self.config_config['log_file'] = parse_value_with_default(
                    content=self.file_content['config'], key='log_file', default_value=default_data.Config.log_file)

                self.config_config['entry_exist'] = parse_value_with_default(content=self.file_content['config'],
                                                                             key='entry_exist',
                                                                             default_value=
                                                                             default_data.Config.entry_exist)
            else:
                self.config_config['wait'] = default_data.Config.wait
                self.config_config['log_level'] = default_data.Config.log_level
                self.config_config['log_file'] = default_data.Config.log_file
                self.config_config['entry_exist'] = default_data.Config.entry_exist

            logging.debug(msg="config-wait " + str(self.config_config['wait']))
            logging.debug(msg="config-log_level " + str(self.config_config['log_level']))
            logging.debug(msg="config-log_file " + str(self.config_config['log_file']))
            logging.debug(msg="config-entry_exist " + str(self.config_config['entry_exist']))
        except KeyError:
            logging.error("Config file error / Config / KeyError")
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

        if 'static_entry' in self.file_content:
            logging.info(msg="data entry found")
            self.parser_static_entry()

        self.parse_api()
        self.parse_config()
        logging.info("Config loaded")
