import logging
import glob
import os


import yaml
from yaml.loader import SafeLoader

from app.utils import parse_value_with_default, check_linux_permissions, parse_logging_level, match_port_to_protocol
from app.data import default
from app.data.validator import validate_ip, validate_domain, validate_network_port, validate_http_response_code, \
    validate_dns_rewrite, validate_ips
from app.data.jobs_configurations import JobsConfs
from app.data.api_configuration import ApiConfiguration
from app.data.config import Config


class ConfigParser:
    """
    Read and parse config file. Run .parse() to run all parses.
    """

    def __init__(self, file: str, jobs_confs: JobsConfs, api_confs: ApiConfiguration, confs: Config):
        """
        :param file: path to config file
        """
        self.config_file = file
        self.JobConfs = jobs_confs
        self.ApiConfs = api_confs
        self.Confs = confs

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
            with open(file=filename, mode="r") as f:
                content_of_file = f.read()

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

        for jobs in self.file_content['http_jobs']:

            try:
                job = jobs['job']
                domain = job['domain']
                answers = job['answers']

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

            data_valid = validate_domain(domain=domain) and validate_ips(ips=answers) and validate_network_port(
                port=port) and validate_http_response_code(code=status_code)
            if data_valid:
                self.JobConfs.JobsHttp.append(interval=interval, status_code=status_code, proto=proto, domain=domain,
                                              answers=answers, timeout=timeout, port=port)
            else:
                logging.info(f"Job for domain: {domain} not added, due to invalid parameters")

    def parse_ping(self):
        """
        Parse ping job, create dictionary compatible with run_jobs.py
        :return:
        """

        for jobs in self.file_content['ping_jobs']:
            try:
                job = jobs['job']
                domain = job['domain']
                answers = job['answers']

                interval = parse_value_with_default(content=job, key='interval',
                                                    default_value=default.PingJob.interval)
                timeout = parse_value_with_default(content=job, key='timeout',
                                                   default_value=default.PingJob.timeout)
                count = parse_value_with_default(content=job, key='count',
                                                 default_value=default.PingJob.count)

                privileged = parse_value_with_default(content=job, key='privileged',
                                                      default_value=default.PingJob.privileged)

            except KeyError:
                logging.error("Error in config file, ping_jobs KeyError")
                break

            data_valid = validate_domain(domain=domain) and validate_ips(ips=answers)

            if data_valid:
                self.JobConfs.JobsPing.append(interval=interval, count=count, timeout=timeout, domain=domain,
                                              answers=answers, privileged=privileged)

            else:
                logging.info(f"Job for domain: {domain} not added, due to invalid parameters")

    def parser_static_entry(self):
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
                self.JobConfs.JobsStaticEntry.append(interval=interval, domain=domain, answer=answer)

            else:
                logging.info(msg=f"Job for domain: {domain} not added, due to invalid parameters")

    def parse_api(self):
        """
        Parse api configuration
        :return:
        """
        try:
            api = self.file_content['api']
            host = api['host']
            username = str(api['username'])
            passwd = str(api['passwd'])

            proto = parse_value_with_default(content=api, key='proto',
                                             default_value=default.Api.proto)
            port = parse_value_with_default(content=api, key='port',
                                            default_value=default.Api.port)
            timeout = parse_value_with_default(content=api, key='timeout',
                                               default_value=default.Api.timeout)

            startup = parse_value_with_default(content=api, key='startup',
                                               default_value=default.Api.startup)

            data_valid = validate_ip(ip=host) or validate_domain(domain=host)
            data_valid = data_valid and validate_network_port(port=port)
            if data_valid:
                self.ApiConfs.set(host=host, username=username, passwd=passwd, proto=proto, timeout=timeout, port=port,
                                  startup_enable=startup)
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
                wait = parse_value_with_default(
                    content=self.file_content['config'], key='wait', default_value=default.Config.wait)
                log_level = parse_value_with_default(
                    content=self.file_content['config'], key="log_level", default_value=default.Config.log_level,
                    cast_type=False)

                log_level = parse_logging_level(logging_str=log_level)
                log_file = parse_value_with_default(
                    content=self.file_content['config'], key='log_file', default_value=default.Config.log_file)

                entry_exist = parse_value_with_default(content=self.file_content['config'],
                                                       key='entry_exist',
                                                       default_value=default.Config.entry_exist)
            else:
                wait = default.Config.wait
                log_level = default.Config.log_level
                log_file = default.Config.log_file
                entry_exist = default.Config.entry_exist

            self.Confs.set(wait=wait, log_level=log_level, log_file=log_file, entry_exist=entry_exist)

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
