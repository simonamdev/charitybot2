import json
import os
import random

import requests

from charitybot2.storage.logging_service import service_url, service_port
from charitybot2.storage.logs_db import LogsDB, Log

service_full_url = 'http://' + service_url + ':' + str(service_port) + '/'
print('Microservice URL is: {}'.format(service_full_url))

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db', 'logs.db')

# Enter debug mode to override the db path
data = {
    'db_path': db_path
}
r = requests.post(url=service_full_url + 'debug', json=data)
assert r.content == b'Successfully entered debug mode'


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
        assert True is json.loads(response.content.decode('utf-8'))['db']


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


class TestLoggingServiceStopping:
    def test_destroy_service(self):
        response = requests.get(url=service_full_url + 'destroy')
        assert b'Shutting down service' == response.content
