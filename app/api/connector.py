import logging
import time
import requests
from requests.auth import HTTPBasicAuth

from app.utils import check_protocol_slashed


class ApiConnector:
    """
    Realize connection between script and adguardhome, add, remove or change dns rewrite entries
    """

    def __init__(self, config: dict):
        """
        :param config: dictionary contains all configuration needed to communicate with adguard api.
                       Syntax:
                        {
                            'host': # adguard ip
                            'port': # connection port (default 80)
                            'proto': # api protocol http or https (default http)
                            'username': # admin user name
                            'passwd': # admin password
                            'timeout': # connection timeout, if any request will exceed this value will be treated as
                                        # a failure
                            'startup':{
                                'test': # set True to test connection to api on start (default True)
                                'timeout': # Timeout of test connection (default 10)
                                'exit_on_fail': # Exit when test connection fail, if set to False test connection
                                                # will run in loop until success (default False)
                                'retry_after': # time to repeat next test connection if previous test fails (default 10)
                                }

                        }
        """
        self.host = check_protocol_slashed(config['proto']) + config['host'] + ":" + str(config['port'])
        self.auth = HTTPBasicAuth(config['username'], config['passwd'])

        self.timeout = config['timeout']

        test_connection = config['startup']['test']
        exit_on_fail = config['startup']['exit_on_fail']
        retry_after = config['startup']['retry_after']
        self.test_timeout = config['startup']['timeout']

        if test_connection:
            if exit_on_fail:
                if self.test_connection() is False:
                    exit(-1)

            while self.test_connection() is False:
                time.sleep(retry_after)

    def test_connection(self):
        """
        Check if connection to AdGuardHome can be established
        :return: True if connection was successful, False if connection was failure
        """
        url = self.host + "/control/status"
        try:
            response = requests.get(url=url, auth=self.auth, timeout=self.timeout)

            if response.status_code != 200:
                logging.error(msg=f"Api test fail status code: {response.status_code}")
                return False
            else:
                logging.info(msg="Api test successful")
                return True

        except requests.ConnectionError:
            logging.error(msg="Can't establish connection to API")
            return False

    def entry_exist(self, answer: str, domain: str):
        """
        Check if provided entry (answer and domain) exist in rewrite list. Check is simple '1:1 check',
        :param answer: dns answer
        :param domain: dns domain
        :return: True if entry exist, False if not, None when request status code was other than 200
        """
        url = self.host + "/control/rewrite/list"
        try:
            response = requests.get(url=url, auth=self.auth, timeout=self.timeout)

            if response.status_code == 200:
                for entry in response.json():

                    if entry["domain"] == domain and entry["answer"] == answer:
                        return True

                return False

            else:
                logging.error(msg=f"Server responded with status code: {response.status_code}")
                return None

        except requests.exceptions.ConnectionError as e:
            logging.error(e)
            return None

    def domain_exist(self, domain: str):
        """
        Check if provided domain exist in rewrite list. Check is simple '1:1 check',
        :param domain: domain to check
        :return: True if domain exist, False if not, None when request status code was other than 200
        """
        url = self.host + "/control/rewrite/list"
        try:
            response = requests.get(url=url, auth=self.auth, timeout=self.timeout)

            if response.status_code == 200:
                for entry in response.json():

                    if entry["domain"] == domain:
                        return True

                return False

            else:
                logging.error(msg=f"Server responded with status code: status code: {response.status_code}")
                return None

        except requests.exceptions.ConnectionError as e:
            logging.error(e)
            return None

    def get_answer_of_domain(self, domain: str):
        """
        Return dns answer of provided domain
        :param domain: domain to check
        :return: str: dns answer (ip address), bool: False if domain not exist or N
                      one when request status code was other than 200
        """
        url = self.host + "/control/rewrite/list"
        try:
            response = requests.get(url=url, auth=self.auth, timeout=self.timeout)

            if response.status_code == 200:
                for entry in response.json():

                    if entry["domain"] == domain:
                        return entry["answer"]

                return False

            else:
                logging.error(msg=f"Server responded with status code: {response.status_code}")
                return None

        except requests.exceptions.ConnectionError as e:
            logging.error(e)
            return None

    def delete_entry(self, answer: str, domain: str):
        """
        Remove rewrite entry
        :param answer: dns answer
        :param domain: dns domain
        :return: True if deletion was successful, False if deletion wasn't successful (for ex. entry does not exist),
                 None if request status code was other than 200
        """
        logging.info(msg=f"Processing entry (remove) {domain} {answer}")
        exist = self.entry_exist(answer=answer, domain=domain)

        if exist:
            url = self.host + "/control/rewrite/delete"
            data = {
                "domain": domain,
                "answer": answer
            }
            response = requests.post(url=url, json=data, auth=self.auth, timeout=self.timeout)
            if response.status_code == 200:
                logging.info(msg="Deletion of entry successful")
                return True
            else:
                logging.info(msg="Deletion of entry failed, server status code: {response.status_code}")
                return None

        elif exist is None:
            logging.info(msg="Deletion of entry failed due to previous errors")
            return None
        else:
            logging.info(msg="Deletion of entry failed (does entry exist ?)")
            return False

    def add_entry(self, answer: str, domain: str):
        """
        Add rewrite entry
        :param answer: dns answer
        :param domain: dns domain
        :return: True if entry was added successful, False if entry wasn't added (for ex. entry exist)
                 None if other error (such as connection error) occurs
        """
        logging.info(msg=f"Processing entry (add) {domain} {answer}")
        exist = self.entry_exist(answer=answer, domain=domain)

        if not exist:
            url = self.host + "/control/rewrite/add"
            data = {
                "domain": domain,
                "answer": answer
            }
            response = requests.post(url=url, json=data, auth=self.auth, timeout=self.timeout)
            if response.status_code == 200:
                logging.info(msg="Adding of entry successful")
                return True
            else:
                logging.info(msg=f"Adding of entry failed, server status code: {response.status_code}")
                return None

        elif exist is None:
            logging.info(msg="Adding of entry failed due to previous errors")
            return None

        else:
            logging.info(msg="Adding of entry failed (does entry exist ?)")
            return False

    def change_entry_answer(self, new_answer: str, old_answer: str, domain: str):
        """
        Change answer of dns rewrite entry
        :param new_answer: dns answer after change
        :param old_answer: actual dns answer
        :param domain: dns domain
        :return: True if change was successful , False if change wasn't successful
                 None if other error (such ad invalid passwd or network connection error) occurs
        """
        logging.info(msg=f"Processing entry (change) {domain} from {old_answer} to {new_answer}")

        status = self.entry_exist(answer=old_answer, domain=domain)
        if status is not True:
            return status

        status = self.delete_entry(answer=old_answer, domain=domain)
        if status:
            status = self.add_entry(answer=new_answer, domain=domain)
            return status
        else:
            return status
