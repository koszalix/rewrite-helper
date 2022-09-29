from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
from typing import Union


class Config:
    """
    Store miscellaneous program configurations
    """
    __wait = 0
    __entry_exist = ""
    __log_file = ""
    __log_level = ""

    def set(self, wait: int, entry_exist: str, log_file: str, log_level: Union[DEBUG, INFO, WARNING, ERROR, CRITICAL]) -> None:
        """
        Set miscellaneous program configurations

        :param wait: specify time to wait before jobs
        :param entry_exist: set what to do when domain is registered in AdGuardHome but answer don't match to any of answers
                            from config file.
        :param log_file: log file
        :param log_level: log level
        :return:
        """
        self.__wait = wait
        self.__entry_exist = entry_exist
        self.__log_file = log_file
        self.__log_level = log_level

    def wait(self) -> int:
        return self.__wait

    def entry_exist(self) -> str:
        return self.__entry_exist

    def log_file(self) -> str:
        return self.__log_file

    def log_level(self) -> Union[DEBUG, INFO, WARNING, ERROR, CRITICAL]:
        return self.__log_level
