import unittest

from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL

from src.parsers.CliParser import CliParser
from src.parsers.CliParser import parse_logging_level


class TestParseLoggingLevel(unittest.TestCase):

    def test_debug(self):
        self.assertEqual(parse_logging_level("DEBUG"), DEBUG)

    def test_info(self):
        self.assertEqual(parse_logging_level("INFO"), INFO)

    def test_warning(self):
        self.assertEqual(parse_logging_level("WARNING"), WARNING)

    def test_error(self):
        self.assertEqual(parse_logging_level("ERROR"), ERROR)

    def test_critical(self):
        self.assertEqual(parse_logging_level("CRITICAL"), CRITICAL)

    def test_unrecognised(self):
        self.assertEqual(parse_logging_level(" test"), False)

    def test_unrecognised_2(self):
        self.assertEqual(parse_logging_level(" DEBUG"), False)

    def test_unrecognised_3(self):
        self.assertEqual(parse_logging_level("DEBUG "), False)

    def test_number(self):
        self.assertEqual(parse_logging_level(3), False)


class TestCliParser(unittest.TestCase):
    def setUp(self):
        # Correct args sets
        self.args_set_0 = ['main.py', '--log-file=file.log', '--log-level=DEBUG', '--privileged', 'config-file']
        self.args_set_1 = ['main.py', '--log-file=file.log', '--log-level=DEBUG', '-p', 'config-file']
        self.args_set_2 = ['main.py', '--log-file=file.log', 'config-file']
        self.args_set_3 = ['main.py', '--log-level=DEBUG', 'config-file']
        self.args_set_4 = ['main.py', '--privileged', 'config-file']
        self.args_set_5 = ['main.py', '-p', 'config-file']
        self.args_set_6 = ['main.py', '--log-file=file.log', '--log-level=DEBUG', '--privileged', 'config-file']

        # Incorrect args sets
        self.args_set_7 = ['main.py', 'config-file', 'config-file-2']
        self.args_set_8 = ['main.py']

        # Args sets for testing help
        self.args_set_9 = ['main.py', '--help', '-p', 'config file']
        self.args_set_10 = ['main.py', '-p', 'config file', '--help']

        self.parser_0 = CliParser(self.args_set_0)
        self.parser_1 = CliParser(self.args_set_1)
        self.parser_2 = CliParser(self.args_set_2)
        self.parser_3 = CliParser(self.args_set_3)
        self.parser_4 = CliParser(self.args_set_4)
        self.parser_5 = CliParser(self.args_set_5)
        self.parser_6 = CliParser(self.args_set_6)

        self.parser_7 = CliParser(self.args_set_7)
        self.parser_8 = CliParser(self.args_set_8)

        self.parser_9 = CliParser(self.args_set_9)
        self.parser_10 = CliParser(self.args_set_10)

        self.parser_0.find_args()
        self.parser_1.find_args()
        self.parser_2.find_args()
        self.parser_3.find_args()
        self.parser_4.find_args()
        self.parser_5.find_args()
        self.parser_6.find_args()

    def test_privileged(self):
        """
        Test if '-p' and '--privileged' arguments are recognised correctly
        :return:
        """
        self.assertEqual(self.parser_0.run_privileged, True)
        self.assertEqual(self.parser_1.run_privileged, True)
        self.assertEqual(self.parser_2.run_privileged, False)
        self.assertEqual(self.parser_3.run_privileged, False)
        self.assertEqual(self.parser_4.run_privileged, True)
        self.assertEqual(self.parser_5.run_privileged, True)
        self.assertEqual(self.parser_6.run_privileged, True)

    def test_log_file(self):
        """
        Test if '--log-file' argument and it's value are recognised correctly
        :return:
        """
        self.assertEqual(self.parser_0.log_file, "file.log")
        self.assertEqual(self.parser_1.log_file, "file.log")
        self.assertEqual(self.parser_2.log_file, "file.log")
        self.assertEqual(self.parser_3.log_file, "")
        self.assertEqual(self.parser_4.log_file, "")
        self.assertEqual(self.parser_5.log_file, "")
        self.assertEqual(self.parser_6.log_file, "file.log")

    def test_log_level(self):
        """
        Test if '--log-level' argument, and it's value are recognised correctly
        :return:
        """
        self.assertEqual(self.parser_0.log_level, DEBUG)
        self.assertEqual(self.parser_1.log_level, DEBUG)
        self.assertEqual(self.parser_2.log_level, INFO)
        self.assertEqual(self.parser_3.log_level, DEBUG)
        self.assertEqual(self.parser_4.log_level, INFO)
        self.assertEqual(self.parser_5.log_level, INFO)
        self.assertEqual(self.parser_6.log_level, DEBUG)

    def test_config_file(self):
        """
        Test if config file is recognised correctly
        :return:
        """
        self.assertEqual(self.parser_0.config_file, "config-file")
        self.assertEqual(self.parser_1.config_file, "config-file")
        self.assertEqual(self.parser_2.config_file, "config-file")
        self.assertEqual(self.parser_3.config_file, "config-file")
        self.assertEqual(self.parser_4.config_file, "config-file")
        self.assertEqual(self.parser_5.config_file, "config-file")
        self.assertEqual(self.parser_6.config_file, "config-file")

    def test_wrong_usage(self):
        """
        Test behavior when wrong count of arguments is provided or unrecognised arguments are used
        :return:
        """
        with self.assertRaises(SystemExit):
            self.parser_7.find_args()
        with self.assertRaises(SystemExit):
            self.parser_8.find_args()

    def test_help(self):
        """
        Test if help is displayed
        :return:
        """
        with self.assertRaises(SystemExit):
            self.parser_9.find_args()
        with self.assertRaises(SystemExit):
            self.parser_10.find_args()


if __name__ == "__main__":
    unittest.main()
