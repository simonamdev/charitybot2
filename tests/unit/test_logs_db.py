import pytest

from charitybot2.storage.logs_db import LogsDB, Log
from tests.tests import TestFilePath, ResetDB

logs_db_path = TestFilePath().get_db_path('logs.db')
logs_sql_path = TestFilePath().get_db_path('logs.sql')


def setup_module():
    ResetDB(db_path=logs_db_path, sql_path=logs_sql_path)


logs_db = LogsDB(db_path=logs_db_path, verbose=True)


class TestLogsDatabaseTableCRUD:
    def test_get_logs_from_empty_database_returns_no_logs(self):
        logs = logs_db.get_all_logs()
        assert isinstance(logs, list)
        assert 0 == len(logs)

    def test_insert_one_log(self):
        logs_db.log(source='test', event='test', level=Log.info_level, message='test')
        logs = logs_db.get_all_logs()
        assert 1 == len(logs)
        assert isinstance(logs[0], Log)
