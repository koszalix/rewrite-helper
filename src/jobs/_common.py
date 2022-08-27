from src.api.ApiConnector import ApiConnector

import logging


class Common:
    """
    Common method for other classes
    """

    def __init__(self, dns_domain="", dns_answer="", dns_answer_failover=None, api_connect=ApiConnector):
        """
        Create configuration variables
        :param dns_domain: str: domain which is used in dns rewrite
        :param dns_answer: str: default (primary) dns answers
        :param dns_answer_failover: list(str): dns answers in case when host on primary
        :param api_connect: configured ApiConnector class
        """

        self.dns_domain = dns_domain
        self.dns_answer_primary = dns_answer
        self.dns_answer_failover = dns_answer_failover

        self.primary_answer_status = None
        self.failover_answer_statuses = [None for _ in range(0, len(dns_answer_failover))]

        self.api_connector = api_connect

        self.actual_dns_answer = False

        self._any_entry_exist()

    def _any_entry_exist(self):
        """
        Check if any of provided entries exist, if entry does not exist create it,
        by default entry with primary dns answer will be created
        :return:
        """
        if self.api_connector.entry_exist(answer=self.dns_answer_primary, domain=self.dns_domain):
            self.actual_dns_answer = self.dns_answer_primary
        else:
            for host in self.dns_answer_failover:
                if self.api_connector.entry_exist(answer=host, domain=self.dns_domain):
                    self.actual_dns_answer = host
                    return
            # no host was found create a new one
            self.api_connector.rewrite_add(domain=self.dns_domain, answer=self.dns_answer_primary)
            self.actual_dns_answer = self.dns_answer_primary

    def api_callback(self):
        """
        Decide if IP address in dns rewrite needs to be changed,
        change dns rewrite answer if needed
        :return:
        """

        if self.primary_answer_status is False:
            for host_id in range(0, len(self.dns_answer_failover)):
                if self.failover_answer_statuses[host_id] is True:
                    if self.actual_dns_answer != self.dns_answer_failover[host_id]:
                        logging.info(
                            "Rewriting for " + self.dns_domain + " from " + str(self.actual_dns_answer) + " to " +
                            self.dns_answer_failover[host_id])
                        change_status = self.api_connector.rewrite_change_answer(old_answer=self.actual_dns_answer,
                                                                                 new_answer=self.dns_answer_failover[
                                                                                     host_id],
                                                                                 domain=self.dns_domain)
                        if change_status:
                            self.actual_dns_answer = self.dns_answer_failover[host_id]
                        return
                    else:
                        return

        if (self.primary_answer_status is True) and self.actual_dns_answer != self.dns_answer_primary:
            change_status = self.api_connector.rewrite_change_answer(old_answer=self.actual_dns_answer,
                                                                     new_answer=self.dns_answer_primary,
                                                                     domain=self.dns_domain)
            if change_status:
                self.actual_dns_answer = self.dns_answer_primary

        # in case when entry not exist due to server unreachable or person who delete entry from AdGuardHome web ui
        self._any_entry_exist()
