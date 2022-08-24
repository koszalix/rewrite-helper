class CliParser:
    """
    Parse command line arguments
    """
    def __init__(self, args):
        self.argv = args
        self.run_privileged = False
        self.config_file = ""

    def print_help(self):

        print("DNS Rewrite helper")
        print("Usage:", self.argv[0], "[options] <config file>")
        print("Options")
        print("\t--privileged, -p run in privileged mode (need to run by root user)")
        exit(0)

    def find_args(self):
        if len(self.argv) <= 1 or len(self.argv) > 3:
            self.print_help()

        for arg in self.argv[1:]:
            if arg == "-p" or arg == "--privileged":
                self.run_privileged = True
            else:
                self.config_file = arg
