import unittest

from app.data.jobs_configurations import JobsConfs


class TestJobsConfsHttp(unittest.TestCase):
    def setUp(self) -> None:
        self.confs = JobsConfs()
        self.confs.JobsHttp.append(interval=2, status_code=3, proto="http", domain="x", answers=["1", "2"], timeout=0.3,
                                   port=33)
        self.confs.JobsHttp.append(interval=12, status_code=13, proto="https", domain="xs", answers=["11", "21"],
                                   timeout=1.3, port=133)

    def test_interval(self):
        self.assertEqual(self.confs.JobsHttp[0].interval(), 2)
        self.assertEqual(self.confs.JobsHttp[1].interval(), 12)

    def test_status_code(self):
        self.assertEqual(self.confs.JobsHttp[0].status_code(), 3)
        self.assertEqual(self.confs.JobsHttp[1].status_code(), 13)

    def test_proto(self):
        self.assertEqual(self.confs.JobsHttp[0].proto(), "http://")
        self.assertEqual(self.confs.JobsHttp[1].proto(), "https://")

    def test_domain(self):
        self.assertEqual(self.confs.JobsHttp[0].domain(), "x")
        self.assertEqual(self.confs.JobsHttp[1].domain(), "xs")

    def test_answers(self):
        self.assertEqual(self.confs.JobsHttp[0].answers(), ['1', '2'])
        self.assertEqual(self.confs.JobsHttp[1].answers(), ['11', '21'])

    def test_timeout(self):
        self.assertLess(abs(self.confs.JobsHttp[0].timeout() - 0.3), 0.001)
        self.assertLess(abs(self.confs.JobsHttp[1].timeout() - 1.3), 0.001)

    def test_port(self):
        self.assertEqual(self.confs.JobsHttp[0].port(), 33)
        self.assertEqual(self.confs.JobsHttp[1].port(), 133)


class TestJobsConfsPing(unittest.TestCase):
    def setUp(self) -> None:
        self.confs = JobsConfs()
        self.confs.JobsPing.append(interval=2, count=3, domain="x", answers=["1", "2"], timeout=0.3,
                                   privileged=False)
        self.confs.JobsPing.append(interval=12, count=13, domain="xs", answers=["11", "21"],
                                   timeout=1.3, privileged=True)

    def test_interval(self):
        self.assertEqual(self.confs.JobsPing[0].interval(), 2)
        self.assertEqual(self.confs.JobsPing[1].interval(), 12)

    def test_count(self):
        self.assertEqual(self.confs.JobsPing[0].count(), 3)
        self.assertEqual(self.confs.JobsPing[1].count(), 13)

    def test_privileged(self):
        self.assertEqual(self.confs.JobsPing[0].privileged(), False)
        self.assertEqual(self.confs.JobsPing[1].privileged(), True)

    def test_timeout(self):
        self.assertLess(abs(self.confs.JobsPing[0].timeout() - 0.3), 0.001)
        self.assertLess(abs(self.confs.JobsPing[1].timeout() - 1.3), 0.001)

    def test_domain(self):
        self.assertEqual(self.confs.JobsPing[0].domain(), "x")
        self.assertEqual(self.confs.JobsPing[1].domain(), "xs")

    def test_answers(self):
        self.assertEqual(self.confs.JobsPing[0].answers(), ['1', '2'])
        self.assertEqual(self.confs.JobsPing[1].answers(), ['11', '21'])


class TestJobsStaticEntry(unittest.TestCase):
    def setUp(self) -> None:
        self.confs = JobsConfs()
        self.confs.JobsStaticEntry.append(interval=2, domain="x", answer="1")
        self.confs.JobsStaticEntry.append(interval=12, domain="xs", answer="21")

    def test_interval(self):
        self.assertEqual(self.confs.JobsStaticEntry[0].interval(), 2)
        self.assertEqual(self.confs.JobsStaticEntry[1].interval(), 12)

    def test_domain(self):
        self.assertEqual(self.confs.JobsStaticEntry[0].domain(), "x")
        self.assertEqual(self.confs.JobsStaticEntry[1].domain(), "xs")

    def test_answers(self):
        self.assertEqual(self.confs.JobsStaticEntry[0].answers(), ['1'])
        self.assertEqual(self.confs.JobsStaticEntry[1].answers(), ['21'])


if __name__ == "__main__":
    unittest.main()
    