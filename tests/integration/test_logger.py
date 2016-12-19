from charitybot2.storage.logger import Logger
from charitybot2.storage.logs_db import Log, LogsDB
from tests.tests import ResetDB, TestFilePath

logs_db_path = TestFilePath().get_db_path('logs.db')
logs_reset_path = TestFilePath().get_db_path('logs.sql')

ResetDB(db_path=logs_db_path, sql_path=logs_reset_path)
logs_db = LogsDB(db_path=logs_db_path, verbose=True)


class TestLoggerValidity:
    def test_logger_logs_successfully(self):
        log = Logger(source='logger_testing', event='logger_testing', debug_db_path=logs_db_path)
        log.log(level=Log.info_level, message='Hello there!')
        logs = logs_db.get_specific_logs(source='logger_testing', level=Log.info_level)
        assert 'Hello there!' in [log.get_message() for log in logs]

    def test_logging_at_various_levels_logs_successfully(self):
        log = Logger(source='logger_level_testing', event='logger_level_testing', debug_db_path=logs_db_path)
        log.log_verbose(message='Info')
        log.log_info(message='Info')
        log.log_warning(message='Warning')
        log.log_error(message='Error')
        verbose_logs = logs_db.get_specific_logs(level=Log.verbose_level, event='logger_level_testing')
        info_logs = logs_db.get_specific_logs(level=Log.verbose_level, event='logger_level_testing')
        warning_logs = logs_db.get_specific_logs(level=Log.verbose_level, event='logger_level_testing')
        error_logs = logs_db.get_specific_logs(level=Log.verbose_level, event='logger_level_testing')
        for log_set in verbose_logs, info_logs, warning_logs, error_logs:
            assert 1 == len(log_set)
            for log in log_set:
                assert 'logger_level_testing' == log.get_event()

    def test_logging_to_console_only_does_not_store_in_db(self):
        log = Logger(source='console_only_testing', event='console_only_testing', console_only=True)
        log.log(level=Log.info_level, message='This should not be in the DB')
        logs = logs_db.get_all_logs()
        for log in logs:
            assert not 'This should not be in the DB' == log.get_message()
