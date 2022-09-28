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

    def set(self, host: str, username: str, passwd: str, proto: str, port: int, timeout: int, startup_enable: bool):
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

    def host(self):
        return self.__host

    def username(self):
        return self.__username

    def passwd(self):
        return self.__passwd

    def proto(self):
        return self.__proto

    def port(self):
        return self.__port

    def timeout(self):
        return self.__timeout

    def startup_enable(self):
        return self.__startup_enable

