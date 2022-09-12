import logging
import glob
import os
import hashlib

import yaml
from yaml.loader import SafeLoader

from src.utils import parse_value_with_default, check_linux_permissions, parse_logging_level, match_port_to_protocol
from src.data import default
from src.data.validator import validate_ip, validate_domain, validate_network_port, validate_http_response_code, \
    validate_dns_rewrite


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
        except (FileNotFoundError, PermissionError, IsADirectoryError, OSError):
            logging.info(f"Can't open config file {filename}")
            return False
        except yaml.YAMLError:
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
                    logging.info(f"Config loaded ({potentially_file})")
                    return True

        return False

    def parse_http(self):
        """
        Parse http jobs, create dictionary compatible with run_jobs.py
        :return:
        """
        job_index = 0
        for jobs in self.file_content['http_jobs']:

            try:
                job = jobs['job']
                self.http_configs[job_index] = {}
                dns_domain = job['domain']
                dns_answer = job['answers']['primary']

                if 'failover' in job['answers']:
                    if job['answers']['failover'] is None:
                        dns_failover = []
                    else:
                        dns_failover = job['answers']['failover']
                else:
                    dns_failover = []

                interval = parse_value_with_default(content=job, key='interval',
                                                    default_value=default.HttpJob.interval)

                status_code = parse_value_with_default(content=job, key='status',
                                                       default_value=default.HttpJob.status)

                proto = parse_value_with_default(content=job, key='proto',
                                                 default_value=default.HttpJob.proto)

                port = parse_value_with_default(content=job, key='port',
                                                default_value=match_port_to_protocol(
                                                    proto=proto, default_port=default.HttpJob.port))

                timeout = parse_value_with_default(content=job, key='timeout',
                                                   default_value=default.HttpJob.timeout)

            except KeyError:
                logging.error("Error in config file, http_jobs KeyError")
                break

            data_valid = validate_dns_rewrite(domain=dns_domain, primary_answer=dns_answer, failover_answers=dns_failover)
            data_valid = data_valid and validate_network_port(port=port)
            data_valid = data_valid and validate_http_response_code(code=status_code)
            if data_valid:

                self.http_configs[job_index] = {}
                self.http_configs[job_index]['dns_domain'] = dns_domain
                self.http_configs[job_index]['dns_answer'] = dns_answer
                self.http_configs[job_index]['dns_answer_failover'] = dns_failover
                self.http_configs[job_index]['interval'] = interval
                self.http_configs[job_index]['status_code'] = status_code
                self.http_configs[job_index]['proto'] = proto
                self.http_configs[job_index]['port'] = port
                self.http_configs[job_index]['timeout'] = timeout

                logging.debug(msg=f"http-domain {self.http_configs[job_index]['dns_domain']}")
                logging.debug(msg=f"http-interval {self.http_configs[job_index]['interval']}")
                logging.debug(msg=f"http-status {self.http_configs[job_index]['status_code']}")
                logging.debug(msg=f"http-proto {self.http_configs[job_index]['proto']}")
                logging.debug(msg=f"http-port {self.http_configs[job_index]['port']}")
                logging.debug(msg=f"http-primary {self.http_configs[job_index]['dns_answer']}")
                logging.debug(msg=f"http-failover " + ' '.join(self.http_configs[job_index]['dns_answer_failover']))
                logging.debug(msg=f"http-timeout {self.http_configs[job_index]['timeout']}")

                job_index = job_index + 1

            else:
                logging.info(f"Job for domain: {dns_domain} not added, due to invalid parameters")

    def parse_ping(self):
        """
        Parse ping job, create dictionary compatible with run_jobs.py
        :return:
        """
        job_index = 0
        for jobs in self.file_content['ping_jobs']:
            try:
                job = jobs['job']
                dns_domain = job['domain']
                dns_answer = job['answers']['primary']

                if 'failover' in job['answers']:
                    if job['answers']['failover'] is None:
                        dns_failover = []
                    else:
                        dns_failover = job['answers']['failover']
                else:
                    dns_failover = []

                interval = parse_value_with_default(content=job, key='interval',
                                                    default_value=default.PingJob.interval)
                timeout = parse_value_with_default(content=job, key='timeout',
                                                   default_value=default.PingJob.timeout)
                count = parse_value_with_default(content=job, key='count',
                                                 default_value=default.PingJob.count)

            except KeyError:
                logging.error("Error in config file, ping_jobs KeyError")
                break

            data_valid = validate_dns_rewrite(domain=dns_domain, primary_answer=dns_answer, failover_answers=dns_failover)

            if data_valid:
                self.ping_configs[job_index] = {}
                self.ping_configs[job_index]['dns_domain'] = dns_domain
                self.ping_configs[job_index]['dns_answer'] = dns_answer
                self.ping_configs[job_index]['dns_answer_failover'] = dns_failover
                self.ping_configs[job_index]['interval'] = interval
                self.ping_configs[job_index]['timeout'] = timeout
                self.ping_configs[job_index]['count'] = count

                logging.debug(msg=f"ping-domain {self.ping_configs[job_index]['dns_domain']}")
                logging.debug(msg=f"ping-interval {self.ping_configs[job_index]['interval']}")
                logging.debug(msg=f"ping-count {self.ping_configs[job_index]['count']}")
                logging.debug(msg=f"ping-timeout {self.ping_configs[job_index]['timeout']}")
                logging.debug(msg=f"ping-primary {self.ping_configs[job_index]['dns_answer']}")
                logging.debug(msg=f"ping-failover " + ' '.join(self.ping_configs[job_index]['dns_answer_failover']))

                job_index = job_index + 1

            else:
                logging.info(f"Job for domain: {dns_domain} not added, due to invalid parameters")

    def parser_static_entry(self):
        job_index = 0
        for jobs in self.file_content['static_entry']:
            try:
                job = jobs['job']

                domain = job['domain']
                answer = job['answer']
                interval = parse_value_with_default(content=job, key='interval',
                                                    default_value=default.StaticEntry.interval)

            except KeyError:
                logging.error("Error in config file, static_entry KeyError")
                break

            data_valid = validate_dns_rewrite(domain=domain, primary_answer=answer, failover_answers=[])

            if data_valid:
                self.static_entry_configs[job_index] = {}
                self.static_entry_configs[job_index]['domain'] = domain
                self.static_entry_configs[job_index]['answer'] = answer
                self.static_entry_configs[job_index]['interval'] = interval

                logging.debug(msg=f"data-entry-domain {self.static_entry_configs[job_index]['domain']}")
                logging.debug(msg=f"data-entry-answer {self.static_entry_configs[job_index]['answer']}")
                logging.debug(msg=f"data-entry-interval {self.static_entry_configs[job_index]['interval']}")

                job_index += 1

            else:
                logging.info(msg=f"Job for domain: {domain} not added, due to invalid parameters")

    def parse_api(self):
        """
        Parse api configuration
        :return:
        """
        try:
            host = self.file_content['api']['host']
            username = self.file_content['api']['username']
            passwd = self.file_content['api']['passwd']

            proto = parse_value_with_default(content=self.file_content['api'], key='proto',
                                             default_value=default.Api.proto)
            port = parse_value_with_default(content=self.file_content['api'], key='port',
                                            default_value=default.Api.port)
            timeout = parse_value_with_default(content=self.file_content['api'], key='timeout',
                                               default_value=default.Api.timeout)
            if 'startup' in self.file_content['api']:
                startup_test = parse_value_with_default(
                    content=self.file_content['api']['startup'],
                    key='test', default_value=default.Api.Startup.test)
                startup_timeout = parse_value_with_default(
                    content=self.file_content['api']['startup'],
                    key='timeout', default_value=default.Api.Startup.timeout)
                startup_exit_on_fall = parse_value_with_default(
                    content=self.file_content['api']['startup'], key='exit_on_fail',
                    default_value=default.Api.Startup.exit_on_false)
                startup_retry_after = parse_value_with_default(
                    content=self.file_content['api']['startup'], key='retry_after',
                    default_value=default.Api.Startup.retry_after)
            else:
                startup_test = True
                startup_timeout = 10
                startup_exit_on_fall = False
                startup_retry_after = 10

            data_valid = validate_ip(ip=host) or validate_domain(domain=host)
            data_valid = data_valid and validate_network_port(port=port)
            if data_valid:
                self.api_config['host'] = host
                self.api_config['username'] = username
                self.api_config['passwd'] = passwd
                self.api_config['proto'] = proto
                self.api_config['port'] = port
                self.api_config['timeout'] = timeout
                self.api_config['startup'] = {}
                self.api_config['startup']['test'] = startup_test
                self.api_config['startup']['timeout'] = startup_timeout
                self.api_config['startup']['exit_on_fail'] = startup_exit_on_fall
                self.api_config['startup']['retry_after'] = startup_retry_after

                logging.debug(msg=f"api-host {self.api_config['host']}")
                logging.debug(msg=f"api-username {self.api_config['username']}")
                logging.debug(msg=f"api-passwd {hashlib.sha256(str(self.api_config['passwd']).encode()).hexdigest()}")
                logging.debug(msg=f"api-proto {self.api_config['proto']}")
                logging.debug(msg=f"api-port {self.api_config['port']}")
                logging.debug(msg=f"api-timeout {self.api_config['timeout']}")
                logging.debug(msg=f"api-startup-test {self.api_config['startup']['test']}")
                logging.debug(msg=f"api-startup-timeout {self.api_config['startup']['timeout']}")
                logging.debug(msg=f"api-startup-exit_on_fail {self.api_config['startup']['exit_on_fail']}")
                logging.debug(msg=f"api-startup-test-retry_after {self.api_config['startup']['retry_after']}")
            else:
                logging.info("Api configuration error")

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
                    content=self.file_content['config'], key='wait', default_value=default.Config.wait)
                log_level = parse_value_with_default(
                    content=self.file_content['config'], key="log_level", default_value="N/A")

                self.config_config['log_level'] = parse_logging_level(logging_str=log_level)

                self.config_config['log_file'] = parse_value_with_default(
                    content=self.file_content['config'], key='log_file', default_value=default.Config.log_file)

                self.config_config['entry_exist'] = parse_value_with_default(content=self.file_content['config'],
                                                                             key='entry_exist',
                                                                             default_value=default.Config.entry_exist)
            else:
                self.config_config['wait'] = default.Config.wait
                self.config_config['log_level'] = default.Config.log_level
                self.config_config['log_file'] = default.Config.log_file
                self.config_config['entry_exist'] = default.Config.entry_exist

            logging.debug(msg=f"config-wait {self.config_config['wait']}")
            logging.debug(msg=f"config-log_level {self.config_config['log_level']}")
            logging.debug(msg=f"config-log_file {self.config_config['log_file']}")
            logging.debug(msg=f"config-entry_exist {self.config_config['entry_exist']}")

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
