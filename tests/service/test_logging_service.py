import json
import os
import random
from pathlib import Path
from time import sleep

import requests
from charitybot2.storage.logging_service import service_url, service_port
from charitybot2.storage.logs_db import LogsDB, Log
from neopysqlite.exceptions import PysqliteTableDoesNotExist
from tests.tests import ServiceTest

service_full_url = 'http://' + service_url + ':' + str(service_port) + '/'
print('Microservice URL is: {}'.format(service_full_url))

current_directory = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_directory, 'db', 'logs.db')
sql_reset_path = os.path.join(current_directory, 'db', 'init_logs_db.sql')
# this can definitely do with its own class to create the paths rather than doing them in each test file
service_script_path = os.path.join(str(Path(os.path.dirname(__file__)).parents[1]), 'charitybot2', 'storage', 'logging_service.py')

service_test = ServiceTest('Logging Service', '', service_path=service_script_path, db_path=db_path,
                           sql_path=sql_reset_path)


def setup_module():
    service_test.start_service()
    # Enter debug mode to override the db path
    data = {
        'db_path': db_path
    }
    r = requests.post(url=service_full_url + 'debug', json=data)
    assert r.content == b'Successfully entered debug mode'


def teardown_module():
    service_test.stop_service()


class TestLoggingServiceBasicResponses:
    def test_service_returns_200_and_responds_with_name_on_base_url(self):
        response = requests.get(url=service_full_url)
        assert 200 == response.status_code
        assert b'Logging Service' == response.content

    def test_service_returns_200_with_health_check(self):
        response = requests.get(url=service_full_url + 'health')
        print(response.content)
        assert 200 == response.status_code


class TestLoggingServiceDebugMode:
    def test_service_is_using_debug_db_path(self):
        response = requests.get(url=service_full_url + 'db')
        assert db_path == response.content.decode('utf-8')

    def test_service_returns_true_on_db_health_check(self):
        response = requests.get(url=service_full_url + 'health')
        assert True is response.json()['db']


class TestLoggingServiceLogging:
    def test_log_request_returns_200_for_empty_body(self):
        minimum_post_data = {
            'event': '',
            'source': '',
            'level': '',
            'message': ''
        }
        response = requests.post(url=service_full_url + 'log', json=minimum_post_data)
        assert 200 == response.status_code
        assert b'Empty Log passed' == response.content

    def test_requesting_without_post_body_throws_500(self):
        response = requests.post(url=service_full_url + 'log', json={})
        assert 500 == response.status_code

    def test_log_request_enters_database_correctly(self):
        test_event_name = 'service_test'
        test_source = 'service_tests'
        test_message = 'Automated service test log message. Random number: ' + str(random.randint(0, 500))
        log_data = {
            'event': test_event_name,
            'source': test_source,
            'level': Log.info_level,
            'message': test_message
        }
        response = requests.post(url=service_full_url + 'log', json=log_data)
        assert 200 == response.status_code
        assert b'Logging successful' == response.content
        test_db = LogsDB(db_path=db_path, event_name=test_event_name, verbose=True)
        logs = test_db.get_all_logs(source=test_source)
        print(logs[-1])
        assert logs[-1].get_event() == test_event_name
        assert logs[-1].get_message() == test_message
        assert logs[-1].get_level() == Log.info_level

    def test_several_log_requests_for_same_event_enter_database_correctly(self):
        message_count_to_log = 20
        log_delay = 0.05
        log_messages = []
        test_event_name = 'flood_test_event'
        test_source = 'flood_test_source'
        test_db = LogsDB(db_path=db_path, event_name=test_event_name, verbose=True)
        try:
            test_db.db.delete_all_rows(table=test_source)
        except PysqliteTableDoesNotExist:
            pass
        log_levels = [Log.info_level, Log.warning_level, Log.error_level]
        for i in range(message_count_to_log):
            message = 'Automated service flood test number {}'.format(i)
            log_messages.append({
                'event': test_event_name,
                'source': test_source,
                'level': random.choice(log_levels),
                'message': message
            })
        for message in log_messages:
            print(message)
            response = requests.post(url=service_full_url + 'log', json=message)
            print(response.status_code)
            assert 200 == response.status_code
            assert b'Logging successful' == response.content
            sleep(log_delay)
        logs = test_db.get_all_logs(source=test_source)
        assert len(logs) == message_count_to_log
        for i in range(message_count_to_log):
            assert logs[i].get_event() == log_messages[i]['event']
            assert logs[i].get_message() == log_messages[i]['message']
            assert logs[i].get_level() == log_messages[i]['level']


class TestLoggingServiceStopping:
    def test_destroy_service(self):
        response = requests.get(url=service_full_url + 'destroy')
        assert b'Shutting down service' == response.content
