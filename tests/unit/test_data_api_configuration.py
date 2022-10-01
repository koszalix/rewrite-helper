import unittest

from app.data.api_configuration import ApiConfiguration


class TestApi(unittest.TestCase):
    def setUp(self):
        self.api_conf = ApiConfiguration()
        self.api_conf.set(host='host', username='username', passwd='passwd', proto='proto', port=80, timeout=0.4,
                          startup_enable=False)

    def test_host(self):
        self.assertEqual(self.api_conf.host(), "host")

    def test_username(self):
        self.assertEqual(self.api_conf.username(), 'username')

    def test_passwd(self):
        self.assertEqual(self.api_conf.passwd(), 'passwd')

    def test_proto(self):
        self.assertEqual(self.api_conf.proto(), 'proto')

    def test_port(self):
        self.assertEqual(self.api_conf.port(), 80)

    def test_timeout(self):
        self.assertLess(abs(self.api_conf.timeout() - 0.4), 0.001)

    def test_startup_enable(self):
        self.assertEqual(self.api_conf.startup_enable(), False)


if __name__ == "__main":
    unittest.main()
