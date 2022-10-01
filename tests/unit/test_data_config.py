import unittest

from app.data.config import Config


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.conf = Config()
        self.conf.set(wait=2, entry_exist="KEEP", log_file="file", log_level=42)

    def test_wait(self):
        self.assertEqual(self.conf.wait(), 2)

    def test_entry_exist(self):
        self.assertEqual(self.conf.entry_exist(), "KEEP")

    def test_log_file(self):
        self.assertEqual(self.conf.log_file(), "file")

    def test_log_level(self):
        self.assertEqual(self.conf.log_level(), 42)
