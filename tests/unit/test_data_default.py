import unittest

from app.data import default


class TestData(unittest.TestCase):
    """
    Check if all api defaults values are correct (those values can be changed accidentally)
    """
    def test_api_proto(self):
        self.assertEqual(default.Api.proto, "http")

    def test_api_port(self):
        self.assertEqual(default.Api.port, 80)

    def test_api_timeout(self):
        self.assertEqual(default.Api.port, 80)

    def test_api_startup_test(self):
        self.assertEqual(default.Api.startup, True)

    def test_config_wait(self):
        self.assertEqual(default.Config.wait, 0)

    def test_config_log_level(self):
        self.assertEqual(default.Config.log_level, False)

    def test_config_log_file(self):
        self.assertEqual(default.Config.log_file, "N/A")

    def test_config_invalid_entry(self):
        self.assertEqual(default.Config.entry_exist, 'KEEP')

    def test_ping_job_interval(self):
        self.assertEqual(default.PingJob.interval, 60)

    def test_ping_job_count(self):
        self.assertEqual(default.PingJob.count, 2)

    def test_ping_job_timeout(self):
        self.assertEqual(default.PingJob.timeout, 2)

    def test_ping_job_privileged(self):
        self.assertEqual(default.PingJob.privileged, False)

    def test_http_job_timeout(self):
        self.assertEqual(default.HttpJob.timeout, 10)

    def test_http_job_interval(self):
        self.assertEqual(default.HttpJob.interval, 60)

    def test_http_job_status(self):
        self.assertEqual(default.HttpJob.status, 200)

    def test_http_job_proto(self):
        self.assertEqual(default.HttpJob.proto, "http")

    def test_http_job_port(self):
        self.assertEqual(default.HttpJob.port, 80)

    def test_static_entry(self):
        self.assertEqual(default.StaticEntry.interval, 60)


if __name__ == '__main__':
    unittest.main()
