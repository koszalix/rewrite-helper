from app.utils import check_protocol_slashed

class DNS:
    """
    Stores DNS answer and domain, answer[0] is primary answer
    """
    __domain = ""
    __answers = []

    def domain(self) -> str:
        return self.__domain

    def answers(self) -> list:
        return self.__answers


class JobHttp(DNS):
    def __init__(self, interval: int, status_code: int, proto: str, domain: str, answers: list, timeout: float,
                 port: int):
        self._interval = interval
        self._status_code = status_code
        self._proto = proto
        self._timeout = timeout
        self._port = port
        self._domain = domain
        self._answers = answers

    def interval(self) -> int:
        return self._interval

    def status_code(self) -> int:
        return self._status_code

    def proto(self) -> str:
        return check_protocol_slashed(proto=self._proto)

    def timeout(self) -> float:
        return self._timeout

    def port(self) -> int:
        return self._port


class JobsHttp:
    """
    Stores configurations for http jobs
    """

    __count = 0
    __http_objs = []

    def append(self, interval: int, status_code: int, proto: str, domain: str, answers: list, timeout: float,
               port: int) -> None:
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
        self.__http_objs.append(JobHttp(interval=interval, status_code=status_code, proto=proto, domain=domain,
                                        answers=answers, timeout=timeout, port=port))

        self.__count += 1

    def __getitem__(self, item) -> JobHttp:
        return self.__http_objs[item]

    def __iter__(self):
        self.__index = 0
        return self

    def __next__(self) -> JobHttp:
        if self.__index >= self.__count:
            raise StopIteration

        temporary_index = self.__index
        self.__index += 1

        return self.__http_objs[temporary_index]


class JobPing(DNS):
    def __init__(self, interval: int, count: int, timeout: float, domain: str, answers: list, privileged: bool):
        self._interval = interval
        self._count = count
        self._timeout = timeout
        self._privileged = privileged
        self.__domain = domain
        self.__answers = answers

    def interval(self) -> int:
        return self._interval

    def count(self) -> int:
        return self._count

    def timeout(self) -> float:
        return self._timeout

    def privileged(self) -> bool:
        return self._privileged


class JobsPing:
    """
    Stores configurations for ping jobs
    """
    __count = 0
    __ping_objs = []

    def append(self, interval: int, count: int, timeout: float, domain: str, answers: list, privileged: bool) -> None:
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

        self.__ping_objs.append(JobPing(interval=interval, count=count, timeout=timeout, domain=domain,
                                        answers=answers, privileged=privileged))

        self.__count += 1

    def __getitem__(self, item) -> JobPing:
        return self.__ping_objs[item]

    def __iter__(self):
        self.__index = 0
        return self

    def __next__(self) -> JobPing:
        if self.__index >= self.__count:
            raise StopIteration

        temporary_index = self.__index
        self.__index += 1

        return self.__ping_objs[temporary_index]


class JobStaticEntry(DNS):
    def __init__(self, interval: int, domain: str, answer: str):
        self.__interval = interval
        self.__domain = domain
        self.__answers = [answer]

    def interval(self) -> int:
        return self.__interval


class JobsStaticEntry:
    """
    Stores configuration for static entry job
    """
    __count = 0
    __se_objs = []

    def append(self, interval: int, domain: str, answer: str) -> None:
        """
        Add new set of config data for static entry

        :param interval: seconds between requests
        :param domain: dns domain
        :param answer: dns answers
        """

        self.__se_objs.append(JobStaticEntry(interval=interval, domain=domain, answer=answer))

    def __getitem__(self, item) -> JobStaticEntry:
        return self.__se_objs[item]

    def __iter__(self):
        self.__index = 0
        return self

    def __next__(self) -> JobStaticEntry:
        if self.__index >= self.__count:
            raise StopIteration

        temporary_index = self.__index
        self.__index += 1

        return self.__se_objs[temporary_index]


class JobsConfs:
    JobsHttp = JobsHttp()
    JobsPing = JobsPing()
    JobsStaticEntry = JobsStaticEntry()
