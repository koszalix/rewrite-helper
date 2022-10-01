class ApiConfiguration:
    """
    Store configuration for Api Connector
    """
    __host = ""
    __username = ""
    __passwd = ""
    __proto = ""
    __port = ""
    __timeout = ""
    __startup_enable = ""

    def set(self, host: str, username: str, passwd: str, proto: str, port: int, timeout: float, startup_enable: bool):
        """
        Set configuration for api

        :param host: ip address of server
        :param username: admin username
        :param passwd: admin passwd
        :param proto: api protocol (http or https)
        :param port: api port
        :param timeout: api connection timeout
        :param startup_enable: enable test of api connection startup
        :return:
        """

        self.__host = host
        self.__username = username
        self.__passwd = passwd
        self.__proto = proto
        self.__port = port
        self.__timeout = timeout
        self.__startup_enable = startup_enable

    def host(self) -> str:
        return self.__host

    def username(self) -> str:
        return self.__username

    def passwd(self) -> str:
        return self.__passwd

    def proto(self) -> str:
        return self.__proto

    def port(self) -> int:
        return self.__port

    def timeout(self) -> float:
        return self.__timeout

    def startup_enable(self) -> bool:
        return self.__startup_enable

