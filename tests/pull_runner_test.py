import nose
import os
import os.path
import unittest
from debmetrics import pull_runner


class pull_runner_test(unittest.TestCase):

    def test_time_series_graph(self):
        """Test creation of timeseries graph"""
        data = [('2014-07-01 01:01:01', '2'), ('2014-07-02 01:01:01', '4')]
        cols = ['ts', 'testing']
        pull_runner.time_series_graph('test', data, cols)
        os.path.isfile(os.path.join('graphs', 'test_timeseries.png'))

    def test_run(self):
        """Test run to ensure no exceptions are raised"""
        pull_runner.run()


if __name__ == '__main__':
    nose.main()
