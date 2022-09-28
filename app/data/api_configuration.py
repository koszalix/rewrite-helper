class ApiConfiguration:
    """
    Store configuration for Api Connector
    """
    host = ""
    username = ""
    passwd = ""
    proto = ""
    port = ""
    timeout = ""
    startup_enable = ""

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

        self.host = host
        self.username = username
        self.passwd = passwd
        self.proto = proto
        self.port = port
        self.timeout = timeout
        self.startup_enable = startup_enable
