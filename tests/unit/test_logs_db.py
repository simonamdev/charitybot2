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

    def test_get_logs_filtered_by_level(self):
        logs_db.log(source='info source', event='info event', level=Log.info_level, message='info message')
        logs_db.log(source='error source', event='error event', level=Log.error_level, message='error message 1')
        logs_db.log(source='error source', event='error event', level=Log.error_level, message='error message 2')
        error_logs = logs_db.get_specific_logs(level=Log.error_level)
        assert 2 == len(error_logs)
        assert 'error message 1' == error_logs[0].get_message()

    def test_get_logs_filtered_by_event(self):
        logs_db.log(source='info', event='info', level=Log.info_level, message='info')
        logs_db.log(source='warning', event='warning', level=Log.warning_level, message='warning')
        logs_db.log(source='error', event='error', level=Log.error_level, message='error')
        warning_event_logs = logs_db.get_specific_logs(event='warning')
        assert 1 == len(warning_event_logs)
        assert 'warning' == warning_event_logs[0].get_source()
        assert 'warning' == warning_event_logs[0].get_message()
        assert 'warning' == warning_event_logs[0].get_event()
        assert Log.warning_level == warning_event_logs[0].get_level()
