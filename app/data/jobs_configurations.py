from app.utils import check_protocol_slashed


class DNS:
    """
    Stores DNS answer and domain, answer[0] is primary answer
    """
    def __init__(self):
        self._domain = ""
        self._answers = []

    def domain(self) -> str:
        return self._domain

    def answers(self) -> list:
        return self._answers


class JobHttp(DNS):
    def __init__(self, interval: int, status_code: int, proto: str, domain: str, answers: list, timeout: float,
                 port: int):
        super().__init__()
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
    def __init__(self):
        self._count = 0
        self._http_objs = []

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
        self._http_objs.append(JobHttp(interval=interval, status_code=status_code, proto=proto, domain=domain,
                                       answers=answers, timeout=timeout, port=port))

        self._count += 1

    def __getitem__(self, item) -> JobHttp:
        return self._http_objs[item]

    def __iter__(self):
        self.__index = 0
        return self

    def __next__(self) -> JobHttp:
        if self.__index >= self._count:
            raise StopIteration

        temporary_index = self.__index
        self.__index += 1

        return self._http_objs[temporary_index]


class JobPing(DNS):
    def __init__(self, interval: int, count: int, timeout: float, domain: str, answers: list, privileged: bool):
        super().__init__()
        self._interval = interval
        self._count = count
        self._timeout = timeout
        self._privileged = privileged
        self._domain = domain
        self._answers = answers

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
    def __init__(self):
        self._count = 0
        self._ping_objs = []

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

        self._ping_objs.append(JobPing(interval=interval, count=count, timeout=timeout, domain=domain,
                                       answers=answers, privileged=privileged))

        self._count += 1

    def __getitem__(self, item) -> JobPing:
        return self._ping_objs[item]

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self) -> JobPing:
        if self._index >= self._count:
            raise StopIteration

        temporary_index = self._index
        self._index += 1

        return self._ping_objs[temporary_index]


class JobStaticEntry(DNS):
    def __init__(self, interval: int, domain: str, answer: str):
        super().__init__()
        self._interval = interval
        self._domain = domain
        self._answers = [answer]

    def interval(self) -> int:
        return self._interval


class JobsStaticEntry:
    """
    Stores configuration for static entry job
    """
    def __init__(self):
        self._count = 0
        self._se_objs = []

    def append(self, interval: int, domain: str, answer: str) -> None:
        """
        Add new set of config data for static entry

        :param interval: seconds between requests
        :param domain: dns domain
        :param answer: dns answers
        """

        self._se_objs.append(JobStaticEntry(interval=interval, domain=domain, answer=answer))

    def __getitem__(self, item) -> JobStaticEntry:
        return self._se_objs[item]

    def __iter__(self):
        self.__index = 0
        return self

    def __next__(self) -> JobStaticEntry:
        if self.__index >= self._count:
            raise StopIteration

        temporary_index = self.__index
        self.__index += 1

        return self._se_objs[temporary_index]


class JobsConfs:
    def __init__(self):
        self.JobsHttp = JobsHttp()
        self.JobsPing = JobsPing()
        self.JobsStaticEntry = JobsStaticEntry()
