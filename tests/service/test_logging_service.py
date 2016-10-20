import json
import os

import requests

from charitybot2.storage.logging_service import service_url, service_port

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
    def test_log_request_returns_200(self):
        response = requests.post(url=service_full_url + 'log')
        assert 200 == response.status_code


class TestLoggingServiceStopping:
    def test_destroy_service(self):
        response = requests.get(url=service_full_url + 'destroy')
        assert b'Shutting down service' == response.content
