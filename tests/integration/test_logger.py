from charitybot2.storage.logger import Logger
from charitybot2.storage.logs_db import Log
from neopysqlite.neopysqlite import Neopysqlite
from tests.tests import ResetDB, TestFilePath

logs_db_path = TestFilePath().get_db_path('logs.db')
logs_reset_path = TestFilePath().get_db_path('logs.sql')

ResetDB(db_path=logs_db_path, sql_path=logs_reset_path)


class TestLoggerValidity:
    def test_logger_logs_successfully(self):
        log = Logger(source='logger_testing', debug_db_path=logs_db_path)
        log.log(level=Log.info_level, message='Hello there!')
        db = Neopysqlite('Log DB', db_path=logs_db_path, verbose=False)
        messages = [log[3] for log in db.get_all_rows(table='logger_testing')]
        assert 'Hello there!' in messages

    def test_logging_at_various_levels_logs_successfully(self):
        log = Logger(source='logger_level_testing', debug_db_path=logs_db_path)
        log.log_info(message='Info')
        log.log_warning(message='Warning')
        log.log_error(message='Error')
        db = Neopysqlite('Log DB', db_path=logs_db_path, verbose=False)
        messages = [{'level': log[2], 'message': log[3]} for log in db.get_all_rows(table='logger_level_testing')]
        assert {'level': Log.info_level, 'message': 'Info'} == messages[0]
        assert {'level': Log.warning_level, 'message': 'Warning'} == messages[1]
        assert {'level': Log.error_level, 'message': 'Error'} == messages[2]

    def test_logging_to_console_only_does_not_store_in_db(self):
        log = Logger(source='console_only_testing', console_only=True)
        log.log(level=Log.info_level, message='This should not be in the DB')
        db = Neopysqlite('Log DB', db_path=logs_db_path, verbose=False)
        messages = [log[3] for log in db.get_all_rows(table='logger_testing')]
        assert 'This should not be in the DB!' not in messages
