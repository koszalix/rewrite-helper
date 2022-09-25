import unittest

from app.api.connector import ApiConnector


class TestApi(unittest.TestCase):
    """
    Test if api connection work correctly, order of those test is IMPORTANT please do not edit it.
    """
    def setUp(self):
        """
        Create ApiConnector objects with variety of config parameters
        :return:
        """
        # Change, depends on your system
        api_configs_correct = {
            'host': '192.168.56.103',
            'port': 80,
            'proto': 'http',
            'username': 'admin',
            'passwd': '12345678',
            'timeout': 10,
            'startup': {
                'test': False,
                'timeout': 5,
                'exit_on_fail': True,
                'retry_after': 10
            }
        }

        api_configs_wrong_auth = {
            'host': '192.168.56.103',
            'port': 80,
            'proto': 'http',
            'username': 'admin',
            'passwd': '123456232',
            'timeout': 10,
            'startup': {
                'test':  False,
                'timeout':  5,
                'exit_on_fail':  True,
                'retry_after': 10
            }
        }
        self.api_correct = ApiConnector(config=api_configs_correct)
        self.api_wrong_auth = ApiConnector(config=api_configs_wrong_auth)

    def test_test_api_connection_correct_auth(self):
        """
        Test behavior of method test_connection with correct authentication
        :return:
        """
        self.assertEqual(self.api_correct.test_connection(), True)

    def test_api_connection_wrong_auth(self):
        """
        Test behavior of method test_connection with incorrect authentication
        :return:
        """
        self.assertEqual(self.api_wrong_auth.test_connection(), False)

    def test_entry_exist_correct_auth_entry_not_exist(self):
        """
        Test behavior of method entry_exist when  authentication is correct but entry don't exist
        :return:
        """
        self.assertEqual(self.api_correct.entry_exist(answer='1.4.4.1', domain='test.lan'), False)

    def test_entry_exist_wrong_auth_entry_not_exist(self):
        """
        Test behavior of method entry_exist when  authentication is incorrect and entry don't exist
        :return:
        """
        self.assertEqual(self.api_wrong_auth.entry_exist(answer='1.1.1.1', domain='test.lan'), None)

    def test_add_entry_correct_auth(self):
        """
        Test behavior of method add_entry when  authentication is correct and entry don't exist
        :return:
        """
        self.assertEqual(self.api_correct.add_entry(answer='1.1.1.1', domain='test.lan'), True)

    def test_add_entry_wrong_auth(self):
        """
        Test behavior of method add_entry when  authentication is incorrect and entry don't exist
        :return:
        """
        self.assertEqual(self.api_wrong_auth.add_entry(answer='1.1.1.1', domain='xtest.lan'), None)

    def test_entry_exist_correct_auth_entry_exist(self):
        """
        Test behavior of method entry_exist when  authentication is correct and entry exist
        :return:
        """
        self.assertEqual(self.api_correct.entry_exist(answer='1.1.1.1', domain='test.lan'), True)

    def test_entry_exist_wrong_auth_entry_exist(self):
        """
        Test behavior of method entry_exist when  authentication is incorrect and entry exist
        :return:
        """
        self.assertEqual(self.api_wrong_auth.entry_exist(answer='1.1.1.1', domain='test.lan'), None)

    def test_add_entry_correct_auth_entry_exist(self):
        """
        Test behavior of method add_entry when authentication is correct and entry exist
        :return:
        """
        self.assertEqual(self.api_correct.add_entry(answer='1.1.1.1', domain='test.lan'), False)

    def test_add_entry_wrong_auth_entry_exist(self):
        """
        Test behavior of method ass_entry when  authentication is incorrect and entry exist
        :return:
        """
        self.assertEqual(self.api_wrong_auth.add_entry(answer='1.1.1.1', domain='test.lan'), None)

    def test_rewrite_change_answer_correct_auth(self):
        """
        Test behavior of method change_entry_answer when  authentication is correct and entry exist
        :return:
        """
        self.assertEqual(self.api_correct.change_entry_answer(new_answer='2.3.4.5', old_answer='1.1.1.1',
                                                              domain='test.lan'), True)

    def test_rewrite_change_answer_correct_auth_entry_not_exist(self):
        """
        Test behavior of method change_entry_answer when  authentication is correct and entry not exist
        :return:
        """
        self.assertEqual(self.api_correct.change_entry_answer(new_answer='2.3.4.5', old_answer='1.5.5.1',
                                                              domain='xd-test.lan'), False)

    def test_rewrite_change_answer_wrong_auth(self):
        """
        Test behavior of method change_entry_answer when  authentication is incorrect and entry exist
        :return:
        """
        self.assertEqual(self.api_wrong_auth.change_entry_answer(new_answer='2.3.4.5', old_answer='1.1.1.1',
                                                                 domain='test.lan'), None)

    def test_rewrite_change_answer_wrong_auth_entry_not_exist(self):
        """
        Test behavior of method change_entry_answer when  authentication is incorrect and entry not exist
        :return:
        """
        self.assertEqual(self.api_wrong_auth.change_entry_answer(new_answer='2.3.4.5', old_answer='1.5.5.1',
                                                                 domain='xd-test.lan'), None)

    def test_rewrite_delete_correct_auth(self):
        """
        Test behavior of method delete_entry when  authentication is correct and entry exist
        :return:
        """
        self.assertEqual(self.api_correct.delete_entry(answer='2.3.4.5', domain='test.lan'), True)

    def test_rewrite_delete_wrong_auth(self):
        """
        Test behavior of method delete_entry when  authentication is incorrect
        :return:
        """
        self.assertEqual(self.api_wrong_auth.delete_entry(answer='2.3.4.5', domain='test.lan'), None)

    def test_rewrite_delete_correct_auth_entry_not_exist(self):
        """
        Test behavior of method delete_entry when  authentication is correct and entry not exist
        :return:
        """
        self.assertEqual(self.api_correct.delete_entry(answer='2.3.4.5', domain='test.lan'), False)

    def test_rewrite_delete_wrong_auth_entry_not_exist(self):
        """
        Test behavior of method delete_entry when  authentication is incorrect and entry not exist
        :return:
        """
        self.assertEqual(self.api_wrong_auth.delete_entry(answer='2.3.4.5', domain='test.lan'), None)

    def test_domain_exist_really_exist_correct_auth(self):
        """
        Test behavior of method domain_exists when domain exist and authentication is correct
        :return:
        """
        self.assertEqual(self.api_correct.domain_exist(domain="do-not.delete"), True)

    def test_domain_exist_not_really_exist_correct_auth(self):
        """
        Test behavior of method domain_exists when domain not exist and authentication is correct
        :return:
        """
        self.assertEqual(self.api_correct.domain_exist(domain="this_domain_not_exist.delete"), False)

    def test_domain_exist_really_exist_wrong_auth(self):
        """
        Test behavior of method domain_exists when domain exist and authentication is incorrect
        :return:
        """
        self.assertEqual(self.api_wrong_auth.domain_exist(domain="do-not.delete"), None)

    def test_domain_exist_not_really_exist_wrong_auth(self):
        """
        Test behavior of method domain_exists when domain not exist and authentication is incorrect
        :return:
        """
        self.assertEqual(self.api_wrong_auth.domain_exist(domain="this_domain_not_exist.delete"), None)

    def test_get_answer_of_domain_exit_correct_auth(self):
        """
        Test behavior of method get_answer_of_domain when domain exist and auth is correct
        :return:
        """
        self.assertEqual(self.api_correct.get_answer_of_domain(domain="do-not.delete"), "1.1.1.1")

    def test_get_answer_of_domain_not_exit_correct_auth(self):
        """
        Test behavior of method get_answer_of_domain when domain not exist and auth is correct
        :return:
        """
        self.assertEqual(self.api_correct.get_answer_of_domain(domain="not-exist.delete"), False)

    def test_get_answer_of_domain_exit_wrong_auth(self):
        """
        Test behavior of method get_answer_of_domain when domain exist and auth is incorrect
        :return:
        """
        self.assertEqual(self.api_wrong_auth.get_answer_of_domain(domain="do-not.delete"), None)

    def test_get_answer_of_domain_not_exit_wrong_auth(self):
        """
        Test behavior of method get_answer_of_domain when domain not exist and auth is incorrect
        :return:
        """
        self.assertEqual(self.api_wrong_auth.get_answer_of_domain(domain="this-domain-not-exist.delete"), None)


if __name__ == "__main__":
    unittest.main()

