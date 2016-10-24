import os

from charitybot2.storage.logger import Logger
from charitybot2.storage.logs_db import Log
from neopysqlite.neopysqlite import Neopysqlite
from tests.tests import ResetDB

current_directory = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_directory, 'db', 'logs.db')
sql_reset_path = os.path.join(current_directory, 'db', 'init_logs_db.sql')

ResetDB(db_path=db_path, sql_path=sql_reset_path)


class TestLoggerValidity:
    def test_logger_logs_successfully(self):
        log = Logger(event='test_logger_event', source='logger_testing', debug_db_path=db_path)
        log.log(level=Log.info_level, message='Hello there!')
        db = Neopysqlite('Log DB', db_path=db_path, verbose=False)
        messages = [log[4] for log in db.get_all_rows(table='logger_testing')]
        assert 'Hello there!' in messages

    def test_logging_at_various_levels_logs_successfully(self):
        log = Logger(event='test_logger_event', source='logger_level_testing', debug_db_path=db_path)
        log.log_info(message='Info')
        log.log_warning(message='Warning')
        log.log_error(message='Error')
        db = Neopysqlite('Log DB', db_path=db_path, verbose=False)
        messages = [{'level': log[2], 'message': log[4]} for log in db.get_all_rows(table='logger_level_testing')]
        assert {'level': Log.info_level, 'message': 'Info'} == messages[0]
        assert {'level': Log.warning_level, 'message': 'Warning'} == messages[1]
        assert {'level': Log.error_level, 'message': 'Error'} == messages[2]

    def test_logging_to_console_only_does_not_store_in_db(self):
        log = Logger(event='test_console_only', source='console_only_testing', console_only=True)
        log.log(level=Log.info_level, message='This should not be in the DB')
        db = Neopysqlite('Log DB', db_path=db_path, verbose=False)
        messages = [log[4] for log in db.get_all_rows(table='logger_testing')]
        assert 'This should not be in the DB!' not in messages
