import logging

import requests
from requests.auth import HTTPBasicAuth

from utils import check_protocol_slashed


class ApiConnector:
    """
    Realize connection between script and adguardhome, add, remove, change dns rewrite entries
    """

    def __init__(self, config={}):
        """
        :param config: dictionary contains all configuration needed to communicate with adguard api.
                       Syntax:
                        {
                            'host': # adguard ip
                            'port': # connection port
                            'proto': # api protocol http or https
                            'username': # admin user name
                            'passwd': # admin password

                        }
        """
        self.host = check_protocol_slashed(config['proto']) + config['host'] + ":" + str(config['port'])
        self.auth = HTTPBasicAuth(config['username'], config['passwd'])
        self.test_connection()

    def test_connection(self):
        """
        Check if script can connect to AdGuardHome api, if not program must exit
        :return: nothing
        """
        url = self.host + "/control/status"
        try:
            response = requests.get(url=url, auth=self.auth)

            if response.status_code != 200:
                if response.status_code == 401:
                    logging.error("Api test fails -> Credentials failure")
                else:
                    logging.error("Api test fails -> status code: " + str(response.status_code))

                exit(-1)
            else:
                logging.info("Api test successful")
        except requests.ConnectionError as e:
            logging.error(e)
            exit(-1)

    def entry_exist(self, answer, domain):
        """
        Check if provided entry (answer and domain) exist in rewrite list. Check is simple '1:1 check',
         wild cards are treated literally
        :param answer: dns answer
        :param domain: dns domain
        :return: True if entry exist, False if not,
                 None when request status code was other than 200
        """
        url = self.host + "/control/rewrite/list"

        try:
            response = requests.get(url=url, auth=self.auth)

            if response.status_code == 200:
                for entry in response.json():

                    if entry["domain"] == domain and entry["answer"] == answer:
                        return True

                return False

            else:
                logging.error("Server responded with status code:", str(response.status_code))
                return None

        except requests.exceptions.ConnectionError as e:
            logging.error(e)
            return None

    def rewrite_delete(self, answer, domain):
        """
        Remove rewrite entry
        :param answer: dns answer
        :param domain: dns domain
        :return: True if deletion was successful, False if deletion wasn't successful (for ex. entry does not exist),
                 None if request status code was other than 200
        """
        logging.info(("Processing entry (remove) " + domain + " " + answer))
        exist = self.entry_exist(answer=answer, domain=domain)

        if exist:
            url = self.host + "/control/rewrite/delete"
            data = {
                "domain": domain,
                "answer": answer
            }
            response = requests.post(url=url, json=data, auth=self.auth)
            if response.status_code == 200:
                logging.info("Deletion of entry successful")
                return True
            else:
                logging.info("Deletion of entry failed, server status code: " + str(response.status_code))
                return None

        elif exist is None:
            logging.info("Deletion of entry failed due to previous errors")
            return None

        else:
            logging.info("Deletion of entry failed (does entry exist ?)")
            return False

    def rewrite_add(self, answer, domain):
        """
        Add rewrite entry
        :param answer: dns answer
        :param domain: dns domain
        :return: True if entry was added successful, False if entry wasn't exist (for ex. entry exist)
                 None if other error occurs
        """
        logging.info(("Processing entry (add) " + domain + " " + answer))
        exist = self.entry_exist(answer=answer, domain=domain)

        if not exist:
            url = self.host + "/control/rewrite/add"
            data = {
                "domain": domain,
                "answer": answer
            }
            response = requests.post(url=url, json=data, auth=self.auth)
            if response.status_code == 200:
                logging.info("Adding of entry successful")
                return True
            else:
                logging.info("Adding of entry failed, server status code: " + str(response.status_code))
                return None

        elif exist is None:
            logging.info("Adding of entry failed due to previous errors")
            return None

        else:
            logging.info("Adding of entry failed (does entry exist ?)")
            return False

    def rewrite_change_answer(self, new_answer, old_answer, domain):
        """
        Change ip of dns rewrite entry
        :param new_answer: dns answer after change
        :param old_answer: actual dns answer
        :param domain: dns domain
        :return: True if change was successful , False if change wasn't successful
                 None if other error occurs
        """
        logging.info(("Processing entry (change) " + domain + " from " + str(old_answer) + " to " + str(new_answer)))

        status = self.rewrite_delete(answer=old_answer, domain=domain)
        if status:
            status = self.rewrite_add(answer=new_answer, domain=domain)
            return status
        else:
            return status
