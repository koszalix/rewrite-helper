import unittest

from src.static import data


class TestData(unittest.TestCase):
    """
    Check if all api defaults values are correct (those values can be changed accidentally)
    """
    def test_api_proto(self):
        self.assertEqual(data.Api.proto, "http")

    def test_api_port(self):
        self.assertEqual(data.Api.port, 80)

    def test_api_timeout(self):
        self.assertEqual(data.Api.port, 80)

    def test_api_startup_test(self):
        self.assertEqual(data.Api.Startup.test, True)

    def test_api_startup_timeout(self):
        self.assertEqual(data.Api.Startup.timeout, 10)

    def test_api_startup_exit_on_false(self):
        self.assertEqual(data.Api.Startup.exit_on_false, False)

    def test_api_startup_retry_after(self):
        self.assertEqual(data.Api.Startup.retry_after, 10)

    def test_config_wait(self):
        self.assertEqual(data.Config.wait, 0)

    def test_config_log_level(self):
        self.assertEqual(data.Config.log_level, False)

    def test_config_log_file(self):
        self.assertEqual(data.Config.log_file, "N/A")

    def test_config_invalid_entry(self):
        self.assertEqual(data.Config.entry_exist, 'KEEP')

    def test_ping_job_interval(self):
        self.assertEqual(data.PingJob.interval, 60)

    def test_ping_job_count(self):
        self.assertEqual(data.PingJob.count, 2)

    def test_ping_job_timeout(self):
        self.assertEqual(data.PingJob.timeout, 2)

    def test_http_job_timeout(self):
        self.assertEqual(data.HttpJob.timeout, 10)

    def test_http_job_interval(self):
        self.assertEqual(data.HttpJob.interval, 60)

    def test_http_job_status(self):
        self.assertEqual(data.HttpJob.status, 200)

    def test_http_job_proto(self):
        self.assertEqual(data.HttpJob.proto, "http")

    def test_http_job_port(self):
        self.assertEqual(data.HttpJob.port, 80)

    def test_static_entry(self):
        self.assertEqual(data.StaticEntry.interval, 60)

if __name__ == '__main__':
    unittest.main()