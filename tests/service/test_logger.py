import os
from pathlib import Path
from time import sleep

import pytest
import requests
from charitybot2.storage.logger import Logger, LoggingFailedException
from charitybot2.storage.logging_service import service_full_url
from charitybot2.storage.logs_db import Log
from neopysqlite.neopysqlite import Neopysqlite
from tests.tests import ServiceTest

current_directory = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_directory, 'db', 'logs.db')
sql_reset_path = os.path.join(current_directory, 'db', 'init_logs_db.sql')
# this can definitely do with its own class to create the paths rather than doing them in each test file
service_script_path = os.path.join(str(Path(os.path.dirname(__file__)).parents[1]), 'charitybot2', 'storage', 'logging_service.py')

service_test = ServiceTest(service_name='Logging Service started by Logger', service_url='',
                           service_path=service_script_path, db_path=db_path, sql_path=sql_reset_path)


def setup_module():
    service_test.start_service()
    # I spent a number of hours trying to figure out why it was not finding the logs database,
    # turns out I have to run the following chunk of code to change it to debug mode
    # this would do good with an eventual refactor and clean up!
    # Enter debug mode to override the db path
    data = {
        'db_path': db_path
    }
    r = requests.post(url=service_full_url + 'debug', json=data)
    assert r.content == b'Successfully entered debug mode'


def teardown_module():
    # requests.get(url='http://127.0.0.1:9000/destroy')
    service_test.stop_service()


class TestLoggerValidity:
    def test_logger_can_connect_to_service(self):
        try:
            log = Logger(event='test_logger_event', source='logger_testing')
        except Exception as e:
            print(e.__traceback__)

    def test_logger_logs_successfully(self):
        log = Logger(event='test_logger_event', source='logger_testing')
        log.log(level=Log.info_level, message='Hello there!')
        db = Neopysqlite('Log DB', db_path=db_path, verbose=False)
        messages = [log[4] for log in db.get_all_rows(table='logger_testing')]
        assert 'Hello there!' in messages

    def test_logging_at_various_levels_logs_successfully(self):
        log = Logger(event='test_logger_event', source='logger_level_testing')
        log.log_info(message='Info')
        log.log_warning(message='Warning')
        log.log_error(message='Error')
        db = Neopysqlite('Log DB', db_path=db_path, verbose=False)
        messages = [{'level': log[2], 'message': log[4]} for log in db.get_all_rows(table='logger_level_testing')]
        assert {'level': Log.info_level, 'message': 'Info'} == messages[0]
        assert {'level': Log.warning_level, 'message': 'Warning'} == messages[1]
        assert {'level': Log.error_level, 'message': 'Error'} == messages[2]

    def test_logger_timing_out_returns_false(self):
        log = Logger(event='test_logger_event', source='logger_testing', timeout=0.0001)
        assert log.log(level=Log.info_level, message='Impossible timeout') is False

    def test_logging_service_unavailable_raises_exception(self):
        log = Logger(event='test_logger_event', source='logger_testing')
        sleep(1)
        requests.get(url='http://127.0.0.1:9000/destroy')
        # service_test.stop_service()
        with pytest.raises(LoggingFailedException):
            log.log(level=1, message='Bla')
