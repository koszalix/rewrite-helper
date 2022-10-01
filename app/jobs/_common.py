from app.api.connector import ApiConnector


class Common:
    """
    Common method for other classes
    """

    def __init__(self, domain: str, answers: list, api_connect: ApiConnector):
        """
        Create configuration variables
        :param domain: domain which is used in dns rewrite
        :param answers
        :param api_connect: configured ApiConnector class
        """

        self.domain = domain
        self.answers = answers

        self.hosts_statuses = []
        self.api_connector = api_connect
        self.actual_dns_answer = ""

    def api_callback(self):
        """
        Decide if IP address in dns rewrite needs to be changed, change dns rewrite answer if needed
        :return:
        """

        for host_status, host_answer in zip(self.hosts_statuses, self.answers):
            if host_status is True:
                answer = self.api_connector.get_answer_of_domain(domain=self.domain)
                if answer is False:
                    if self.api_connector.add_entry(answer=host_answer, domain=self.domain):
                        return
                else:
                    if answer != host_answer:
                        if self.api_connector.change_entry_answer(new_answer=host_answer, old_answer=answer,
                                                                  domain=self.domain):
                            return
                    else:
                        return
        else:
            if len(self.answers) == 1:
                answer = self.api_connector.get_answer_of_domain(domain=self.domain)
                if answer is False:
                    if self.api_connector.add_entry(answer=self.answers[0], domain=self.domain):
                        return
