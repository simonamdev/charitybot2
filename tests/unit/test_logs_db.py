import time
from charitybot2.storage.logs_db import LogsDB, Log
from tests.test_helpers import TestFilePath, ResetDB

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
        logs_db.log(source='info source', event='info event', level=Log.info_level, message='test_level_filter')
        logs_db.log(source='error source', event='error event', level=Log.error_level, message='test_level_filter')
        logs_db.log(source='error source', event='error event', level=Log.error_level, message='test_level_filter')
        logs_db.log(source='verbose source', event='verbose event', level=Log.verbose_level, message='test_level_filter')
        error_logs = logs_db.get_specific_logs(level=Log.error_level)
        assert 2 == len(error_logs)
        for log in error_logs:
            assert 'test_level_filter' == log.get_message()
            assert Log.error_level == log.get_level()
        verbose_logs = logs_db.get_specific_logs(level=Log.verbose_level)
        assert 1 == len(verbose_logs)
        assert 'test_level_filter' == verbose_logs[0].get_message()
        assert Log.verbose_level == verbose_logs[0].get_level()

    def test_get_logs_filtered_by_event(self):
        logs_db.log(source='info', event='info', level=Log.info_level, message='test_event_filter')
        logs_db.log(source='warning', event='warning', level=Log.warning_level, message='test_event_filter')
        logs_db.log(source='error', event='error', level=Log.error_level, message='test_event_filter')
        warning_event_logs = logs_db.get_specific_logs(event='warning')
        assert 1 == len(warning_event_logs)
        assert 'warning' == warning_event_logs[0].get_source()
        assert 'warning' == warning_event_logs[0].get_event()
        assert Log.warning_level == warning_event_logs[0].get_level()
        for log in warning_event_logs:
            assert 'test_event_filter' == log.get_message()

    def test_get_logs_filtered_by_source(self):
        logs_db.log(source='test_source_filter', event='test', level=Log.info_level, message='test_source_filter')
        logs_db.log(source='test_source_filter', event='test', level=Log.warning_level, message='test_source_filter')
        logs_db.log(source='test_source_filter', event='test', level=Log.error_level, message='test_source_filter')
        filtered_logs = logs_db.get_specific_logs(source='test_source_filter')
        assert 3 == len(filtered_logs)
        for log in filtered_logs:
            assert 'test_source_filter' == log.get_message()

    def test_get_logs_filtered_by_time(self):
        # space out from last test
        time.sleep(3)
        logs_db.log(source='time_filter', event='time_filter', level=Log.info_level, message='time_filter')
        logs_db.log(source='time_filter', event='time_filter', level=Log.warning_level, message='time_filter')
        logs_db.log(source='time_filter', event='time_filter', level=Log.error_level, message='time_filter')
        filtered_logs = logs_db.get_specific_logs(timestamp=int(time.time()) - 3)
        assert 3 == len(filtered_logs)
        for log in filtered_logs:
            assert 'time_filter' == log.get_message()
