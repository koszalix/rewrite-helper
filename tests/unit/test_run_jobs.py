import unittest

from app.run_jobs import TestHosts
from app.api.connector import ApiConnector
from app.data.api_configuration import ApiConfiguration
from app.data.jobs_configurations import JobsConfs
from app.data.config import Config


class TestHost(unittest.TestCase):
    def setUp(self):
        api_configs_correct = ApiConfiguration.set(host='192.168.56.103', port=80, proto='http', username='admin',
                                                   passwd='12345678', timeout=10, startup_enable=False)

        api_configs_wrong_auth = ApiConfiguration.set(host='192.168.56.103', port=80, proto='http', username='admin',
                                                      passwd='12343235678', timeout=10, startup_enable=False)

        self.api_correct = ApiConnector(config=api_configs_correct)
        self.api_wrong_auth = ApiConnector(config=api_configs_wrong_auth)

        self.confs_jobs = JobsConfs()
        self.confs_confs = Config()

        # leave tests when basic test entry can't be created
        if self.api_correct.add_entry(domain='test-host.lan', answer="2.2.2.2") is False:
            exit(-1)

    def test_add_task_correct_auth_domain_exist_keep(self):
        """
        Test behavior of add_task when auth is correct domain exist and entry_exist  is set to KEEP
        :return:
        """

        testHost = TestHosts(api_connector=self.api_correct, config_configs=self.confs_confs,
                             jobs_confs=self.confs_jobs)
        # ensure if domain exist, without that test is a little nonsense
        self.assertEqual(self.api_correct.domain_exist(domain="test-host.lan"), True)
        self.assertEqual(testHost.add_task(domain="test-host.lan"), True)

    def test_add_task_correct_auth_domain_not_exist_keep(self):
        """
        Test behavior of add_task when auth is correct domain not exist and entry_exist  is set to KEEP
        :return:
        """
        testHost = TestHosts(api_connector=self.api_correct, config_configs=self.confs_confs,
                             jobs_confs=self.confs_jobs)
        # ensure if domain not exist, without that test is a little nonsense
        self.assertEqual(self.api_correct.domain_exist(domain="inv-test-host.lan"), False)
        self.assertEqual(testHost.add_task(domain="inv-test-host.lan"), True)

    def test_add_task_correct_auth_domain_exist_drop(self):
        """
        Test behavior of add_task when auth is correct domain exist and entry_exist  is set to DROP
        :return:
        """
        testHost = TestHosts(api_connector=self.api_correct, config_configs=self.confs_confs,
                             jobs_confs=self.confs_jobs)
        # ensure if domain exist, without that test is a little nonsense
        self.assertEqual(self.api_correct.domain_exist(domain="test-host.lan"), True)
        self.assertEqual(testHost.add_task(domain="test-host.lan"), False)

    def test_add_task_correct_auth_domain_not_exist_drop(self):
        """
        Test behavior of add_task when auth is correct domain not exist and entry_exist  is set to DROP
        :return:
        """
        testHost = TestHosts(api_connector=self.api_correct, config_configs=self.confs_confs,
                             jobs_confs=self.confs_jobs)
        # ensure if domain not exist, without that test is a little nonsense
        self.assertEqual(self.api_correct.domain_exist(domain="inv-test-host.lan"), False)
        self.assertEqual(testHost.add_task(domain="inv-test-host.lan"), True)

    def test_add_task_correct_auth_domain_exist_delete(self):
        """
        Test behavior of add_task when auth is correct domain exist and entry_exist  is set to DELETE
        :return:
        """
        testHost = TestHosts(api_connector=self.api_correct, config_configs=self.confs_confs,
                             jobs_confs=self.confs_jobs)
        # ensure if domain exist, without that test is a little nonsense
        self.assertEqual(self.api_correct.domain_exist(domain="test-host.lan"), True)

        self.assertEqual(testHost.add_task(domain="test-host.lan"), True)

    def test_add_task_correct_auth_domain_not_exist_delete(self):
        """
        Test behavior of add_task when auth is correct domain not exist and entry_exist  is set to DELETE
        :return:
        """
        testHost = TestHosts(api_connector=self.api_correct, config_configs=self.confs_confs,
                             jobs_confs=self.confs_jobs)
        # ensure if domain not exist, without that test is a little nonsense
        self.assertEqual(self.api_correct.domain_exist(domain="inv-test-host.lan"), False)
        self.assertEqual(testHost.add_task(domain="inv-test-host.lan"), True)

    def test_add_task_wrong_auth_domain_exist_keep(self):
        """
        Test behavior of add_task when auth is incorrect domain exist and entry_exist  is set to KEEP
        :return:
        """
        testHost = TestHosts(api_connector=self.api_wrong_auth, config_configs=self.confs_confs,
                             jobs_confs=self.confs_jobs)
        self.assertEqual(testHost.add_task(domain="test-host.lan"), False)

    def test_add_task_wrong_auth_domain_not_exist_keep(self):
        """
        Test behavior of add_task when auth is incorrect domain exist and entry_exist is set to KEEP
        :return:
        """
        testHost = TestHosts(api_connector=self.api_wrong_auth, config_configs=self.confs_confs,
                             jobs_confs=self.confs_jobs)
        self.assertEqual(testHost.add_task(domain="inv-test-host.lan"), False)

    def test_add_task_wrong_auth_domain_exist_drop(self):
        """
        Test behavior of add_task when auth is incorrect domain exist and entry_exist  is set to DROP
        :return:
        """
        testHost = TestHosts(api_connector=self.api_wrong_auth, config_configs=self.confs_confs,
                             jobs_confs=self.confs_jobs)
        self.assertEqual(testHost.add_task(domain="test-host.lan"), False)

    def test_add_task_wrong_auth_domain_not_exist_drop(self):
        """
        Test behavior of add_task when auth is incorrect domain not exist and entry_exist  is set to DROP
        :return:
        """
        testHost = TestHosts(api_connector=self.api_wrong_auth, config_configs=self.confs_confs,
                             jobs_confs=self.confs_jobs)
        self.assertEqual(testHost.add_task(domain="inv-test-host.lan"), False)

    def test_add_task_wrong_auth_domain_exist_delete(self):
        """
        Test behavior of add_task when auth is incorrect domain exist and entry_exist  is set to DELETE
        :return:
        """
        testHost = TestHosts(api_connector=self.api_wrong_auth, config_configs=self.confs_confs,
                             jobs_confs=self.confs_jobs)
        self.assertEqual(testHost.add_task(domain="test-host.lan"), False)

    def test_add_task_wrong_auth_domain_not_exist_delete(self):
        """
        Test behavior of add_task when auth is incorrect domain not exist and entry_exist is set to DELETE
        :return:
        """
        testHost = TestHosts(api_connector=self.api_wrong_auth, config_configs=self.confs_confs,
                             jobs_confs=self.confs_jobs)
        self.assertEqual(testHost.add_task(domain="inv-test-host.lan"), False)

    def tearDown(self):
        self.api_correct.delete_entry(domain='test-host.lan', answer="2.2.2.2")


if __name__ == "__main__":
    unittest.main()
