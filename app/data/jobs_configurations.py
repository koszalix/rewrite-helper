from typing import Union


class IterationEngine:

    # number of jobs
    __count = 0

    # index used by iterator
    __index = 0

    def _check_idx(self, idx) -> bool:
        """
        Check if idx (job id) is valid

        Idx must be greater or equal to zero and lower than self.__count
        :param idx:
        :return: True
        """
        if 0 <= idx < self.__count:
            return True
        return False

    def __iter__(self):
        self.__index = 0
        return self

    def __next__(self):
        if self.__index >= self.__count:
            raise StopIteration

        temporary_index = self.__index
        self.__index += 1

        return temporary_index


class DNS:
    """
    Stores DNS answer and domain, answer[0] is primary answer
    """
    __domain = ""
    __answers = []

    def domain(self):
        return self.__domain

    def answers(self):
        return self.__answers


class JobHttp(DNS):
    def __init__(self, interval: int, status_code: int, proto: str, domain: str, answers: list, timeout: int, port: int):
        self._interval = interval
        self._status_code = status_code
        self._proto = proto
        self._timeout = timeout
        self._port = port
        self._domain = domain
        self._answers = answers

    def interval(self):
        return self._interval

    def status_code(self):
        return self._status_code

    def proto(self):
        return self._proto

    def timeout(self):
        return self._timeout

    def port(self):
        return self._port


class JobsHttp(DNS, IterationEngine):
    """
    Stores configurations for http jobs
    """
    http_objs = []

    def append(self, interval: int, status_code: int, proto: str, domain: str, answers: list, timeout: int, port: int) -> None:
        """
        Add new set of config data for http job

        :param interval: seconds between requests
        :param status_code: http response status code treated as correct
        :param proto: http transport protocol (http or https)
        :param domain: dns domain
        :param answers: dns answers (first answer is primary)
        :param timeout: request timeout, if timeout is exceeded host request is treated as failed
        :param port: request port
        :return: None
        """
        self.http_objs.append(JobHttp(interval=interval, status_code=status_code, proto=proto, domain=domain, answers=answers, timeout=timeout, port=port))

        self.__count += 1

    def __getitem__(self, item):
        return self.http_objs[item]


class JobPing(DNS):
    def __init__(self, interval: int, count: int, timeout: int, domain: str, answers: list, privileged: bool):
        self._interval = interval
        self._count = count
        self._timeout = timeout
        self._privileged = privileged
        self.__domain = domain
        self.__answers = answers

    def interval(self):
        return self._interval

    def count(self):
        return self._count

    def timeout(self):
        return self._timeout

    def privileged(self):
        return self._privileged


class JobsPing(IterationEngine):
    """
    Stores configurations for ping jobs
    """
    ping_objs = []

    def append(self, interval: int, count: int, timeout: int, domain: str, answers: list, privileged: bool) -> None:
        """
        Add new set of config data for http job

        :param interval: seconds between requests
        :param count: number of packages send by each request
        :param timeout: request timeout, if timeout is exceeded host request is treated as failed
        :param domain: dns domain
        :param answers: dns answers (first answer is primary)
        :param privileged: set True to run in privileged mode, see icmplib documentation for more
        :return: None
        """

        self.ping_objs.append(JobPing(interval=interval, count=count, timeout=timeout, domain=domain, answers=answers, privileged=privileged))

        self.__count += 1

    def __getitem__(self, item):
        return self.ping_objs[item]


class JobStaticEntry(DNS):
    def __init__(self, interval, domain, answer):
        self.__interval = interval
        self.__domain = domain
        self.__answers = [answer]

    def interval(self):
        return self.__interval


class JobsStaticEntry(DNS, IterationEngine):
    """
    Stores configuration for static entry job
    """
    se_objs = []

    def append(self, interval: int, domain: str, answer: str) -> None:
        """
        Add new set of config data for static entry

        :param interval: seconds between requests
        :param domain: dns domain
        :param answer: dns answers
        """

        self.se_objs.append(JobStaticEntry(interval=interval, domain=domain, answer=answer))

    def __getitem__(self, item):
        return self.se_objs[item]


class JobsConfs:
    JobHttp = JobsHttp()
    JobPing = JobsPing()
    JobStaticEntry = JobsStaticEntry()
