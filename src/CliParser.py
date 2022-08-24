from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL

class CliParser:
    """
    Parse command line arguments
    """
    def __init__(self, args):
        """
        :param args: sys.argv arguments
        """
        self.argv = args
        self.run_privileged = False
        self.config_file = ""
        self.log_file = ""
        self.log_level = ""

    def print_help(self):
        """
        Display help information and exit
        :return:
        """
        print("DNS Rewrite helper")
        print("Usage:", self.argv[0], "[options] <config file>")
        print("Options")
        print("\t--help display help and exit")
        print("\t--privileged, -p run in privileged mode (need to run by root user)")
        print("\t--log-file=<file name>, set log output file")
        print("\t--log-level=<level>, set log level")
        print("\t\tavailable levels: DEBUG, INFO, WARNING, ERROR, CRITICAL")
        exit(0)

    def parse_logging_level(self, logging_str):
        """
        Convert from loging level in string to logging object
        :param logging_str: str: logging level
        :return: logging level object or False if can't match level
        """
        if logging_str == "DEBUG":
            return DEBUG
        elif logging_str == "INFO":
            return INFO
        elif logging_str == "WARNING":
            return WARNING
        elif logging_str == "ERROR":
            return ERROR
        elif logging_str == "CRITICAL":
            return CRITICAL
        else:
            return False

    def find_args(self):
        """
        Search specific arguments in sys.arg
        :return:
        """
        if len(self.argv) <= 1 or len(self.argv) > 5:
            self.print_help()

        for arg in self.argv[1:]:
            if arg == "--help":
                self.print_help()

            if arg == "-p" or arg == "--privileged":
                self.run_privileged = True

            elif arg[0:len('--log-file')] == '--log-file':
                self.log_file = arg[len('--log-file')+1:]

            elif arg[0:len('--log-level')] == '--log-level':
                level = self.parse_logging_level(arg[len('--log-level')+1:])
                if level is not False:
                    self.log_level = level
                else:
                    self.log_level = INFO
            else:
                self.config_file = arg
