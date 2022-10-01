from typing import Union


class Config:
    """
    Store miscellaneous program configurations
    """
    def __init__(self):
        self.__wait = 0
        self.__entry_exist = ""
        self.__log_file = ""
        self.__log_level = 0

    def set(self, wait: int, entry_exist: str, log_file: str, log_level: Union[int, bool]) -> None:
        """
        Set miscellaneous program configurations

        :param wait: specify time to wait before jobs
        :param entry_exist: set what to do when domain is registered in AdGuardHome but answer don't match to
                            any of answers from config file.
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

    def log_level(self) -> Union[int, bool]:
        return self.__log_level
