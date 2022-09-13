from logging import INFO

from src.utils import parse_logging_level


class CliParser:
    """
    Parse command line arguments
    """

    def __init__(self, args: list):
        """
        :param args: sys.argv arguments
        """
        self.argv = args
        self.run_privileged = False
        self.config_file = ""
        self.log_file = ""
        self.log_level = INFO

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

    def find_args(self):
        """
        Search specific arguments in sys.arg
        :return:
        """

        config_file_set = False

        if len(self.argv) <= 1 or len(self.argv) > 5:
            self.print_help()

        for arg in self.argv[1:]:
            if arg == "--help":
                self.print_help()

            if arg == "-p" or arg == "--privileged":
                self.run_privileged = True

            elif arg[0:len('--log-file')] == '--log-file':
                self.log_file = arg[len('--log-file') + 1:]

            elif arg[0:len('--log-level')] == '--log-level':
                level = parse_logging_level(arg[len('--log-level') + 1:])
                if level is not False:
                    self.log_level = level
            else:
                if config_file_set is False:
                    self.config_file = arg
                    config_file_set = True
                else:
                    self.print_help()
