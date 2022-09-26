from typing import Union


class JobDescriptor:
    job_id = 0
    job_type = ""


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


class DNS(IterationEngine):
    """
    Stores DNS answer and domain, answer[0] is primary answer
    """
    __domain = []
    __answers = []

    def get_domain(self, idx: int) -> Union[str, bool]:
        """
        Get domain of specific http job

        :param idx: job id
        :return: job interval or False in case of failure (idx is not valid)
        """

        if self._check_idx(idx=idx) is True:
            return False
        return self.__domain[idx]

    def get_answers(self, idx: int) -> Union[list, bool]:
        """
        Get answers (ip addressed) of specific http job

        :param idx: job id
        :return: job interval or False in case of failure (idx is not valid)
        """

        if self._check_idx(idx=idx) is True:
            return False
        return self.__answers[idx]


class JobHttp(DNS, IterationEngine):
    """
    Stores configuration for http job
    """
    __interval = []
    __status_code = []
    __proto = []

    def append(self, interval: int, status_code: int, proto: str, domain: str, answers: list):
        """
        Add new set of config data for http job

        :param interval:
        :param status_code:
        :param proto:
        :param domain:
        :param answers:
        :return:
        """
        self.__interval.append(interval)
        self.__status_code.append(status_code)
        self.__proto.append(proto)
        self.__domain.append(domain)
        self.__answers.append(answers)

        self.__count += 1

    def get_interval(self, idx: int) -> Union[int, bool]:
        """
        Get interval of specific http job

        :param idx: job id
        :return: job interval or False in case of failure (idx is not valid)
        """
        if self._check_idx(idx=idx) is True:
            return False
        return self.__interval[idx]

    def get_status_code(self, idx: int) -> Union[int, bool]:
        """
        Get status_code of specific http job

        :param idx: job id
        :return: job interval or False in case of failure (idx is not valid)
        """
        if self._check_idx(idx=idx) is True:
            return False
        return self.__status_code[idx]

    def get_proto(self, idx: int) -> Union[str, bool]:
        """
        Get protocol of specific http job

        :param idx: job id
        :return: job interval or False in case of failure (idx is not valid)
        """

        if self._check_idx(idx=idx) is True:
            return False
        return self.__proto[idx]


class JobPing(DNS, IterationEngine):
    __interval = []
    __count = []
    __timeout = []
    __privileged = []

    def append(self, interval: int, count: int, timeout: int, domain: str, answers: list, privileged : bool):
        self.__interval.append(interval)
        self.__count.append(count)
        self.__timeout.append(timeout)
        self.__domain.append(domain)
        self.__answers.append(answers)
        self.__privileged.append(privileged)

        self.__count += 1

    def get_interval(self, idx: int) -> Union[int, bool]:
        """
        Get interval of specific http job

        :param idx: job id
        :return: job interval or False in case of failure (idx is not valid)
        """
        if self._check_idx(idx=idx) is True:
            return False
        return self.__interval[idx]

    def get_count(self, idx: int) -> Union[int, bool]:
        """
        Get package count of specific http job

        :param idx: job id
        :return: job interval or False in case of failure (idx is not valid)
        """
        if self._check_idx(idx=idx) is True:
            return False
        return self.__count[idx]

    def get_timeout(self, idx: int) -> Union[int, bool]:
        """
        Get timeout of specific http job

        :param idx: job id
        :return: job interval or False in case of failure (idx is not valid)
        """
        if self._check_idx(idx=idx) is True:
            return False
        return self.__timeout[idx]

    def get_privileged(self, idx: int) -> Union[int, bool]:
        """
        Get state of privileged run of specific http job

        :param idx: job id
        :return: job interval or False in case of failure (idx is not valid)
        """
        if self._check_idx(idx=idx) is True:
            return False
        return self.__privileged[idx]
