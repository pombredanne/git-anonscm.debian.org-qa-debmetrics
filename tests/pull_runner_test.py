import nose
import unittest
from debmetrics import pull_runner
from debmetrics.base import Base


class pull_runner_test(unittest.TestCase):

    def test_table_factory(self):
        a_class = pull_runner.table_factory('vcs')
        assert issubclass(a_class, Base)

    def test_table2class(self):
        assert pull_runner.table2class('releases_count') == 'Releases_Count'

    def test_quote(self):
        assert pull_runner.quote('timestamp') == 'timestamp'
        assert pull_runner.quote('123') == '123'
        assert pull_runner.quote('hello') == "'hello'"

    def test_db_insert(self):
        header = ['ts', 'svn', 'darcs', 'git', 'bzr', 'using_vcs', 'cvs',
                  'mtn', 'total', 'arch', 'hg']
        rows = [['2014-05-28 00:14:48.632243', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]
        table = 'vcs'
        try:
            pull_runner.db_insert(header, rows, table)
        except Exception:
            self.fail('db_insert raised an Exception!')

    def test_handle_csv(self):
        pass

    def test_should_run(self):
        assert pull_runner.should_run('vcs.py', '* * * * *')

    def test_update_last_ran(self):
        pass

    def test_date_to_str(self):
        assert pull_runner.date_to_str(pull_runner.str_to_date('2014-05-01 05:00')) == '2014-05-01 05:00'

    def test_db_fetch(self):
        table = 'vcs'
        try:
            pull_runner.db_fetch(table)
        except Exception:
            self.fail('db_fetch raised an Exception!')

    def test_pack(self):
        pass


if __name__ == '__main__':
    nose.main()
