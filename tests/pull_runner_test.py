import nose
import unittest
from debmetrics import pull_runner
from debmetrics.base import Base


class pull_runner_test(unittest.TestCase):

    def test_table_factory(self):
        """Test to ensure that a class generated by table_factory is a subclass of
        Base
        """
        a_class = pull_runner.table_factory('vcs')
        self.assertTrue(issubclass(a_class, Base))

    def test_table2class(self):
        """Test conversion of table string to class string"""
        self.assertEqual(pull_runner.table2class('releases_count'),
                         'ReleasesCount')

    def test_quote(self):
        """Test quoting of strings sent to the runner"""
        self.assertEqual(pull_runner.quote('timestamp'), 'timestamp')
        self.assertEqual(pull_runner.quote('123'), '123')
        self.assertEqual(pull_runner.quote('hello'), "'hello'")

    def test_db_insert(self):
        """Test for insert of data into database via runner"""
        header = ['ts', 'svn', 'darcs', 'git', 'bzr', 'using_vcs', 'cvs',
                  'mtn', 'total', 'arch', 'hg']
        rows = [['2014-05-28 00:14:48.632243', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]
        table = 'vcs'
        pull_runner.db_insert(header, rows, table)

    def test_handle_csv(self):
        pass

    def test_should_run(self):
        """Test of whether a script should run or not"""
        self.assertTrue(pull_runner.should_run('vcs.py', '* * * * *'))

    def test_update_last_ran(self):
        pass

    def test_date_to_str(self):
        """Test converting a string to a date and back again"""
        adate = pull_runner.str_to_date('2014-05-01 05:00')
        astring = pull_runner.date_to_str(adate)
        self.assertEqual(astring, '2014-05-01 05:00')

    def test_db_fetch(self):
        """Test fetching data from the database via runner"""
        table = 'vcs'
        pull_runner.db_fetch(table)

    def test_pack(self):
        pass


if __name__ == '__main__':
    nose.main()
