import pytest
from charitybot2.exceptions import IllegalArgumentException
from charitybot2.paths import init_test_sql_script_path
from charitybot2.persistence.sql_script import SQLScript


class TestSQLScript:
    def test_passing_non_existent_file_throws_exception(self):
        with pytest.raises(FileNotFoundError):
            sql_script = SQLScript(path='bla/bla.sql')

    def test_reading_sql_file(self):
        sql_script = SQLScript(path=init_test_sql_script_path)
        sql = sql_script.return_sql()
        assert 125 == len(sql)
