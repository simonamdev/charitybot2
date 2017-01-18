import pytest
import requests
from charitybot2.paths import external_api_cli_path
from charitybot2.reporter.external_api.external_api import api_full_url, api_paths
from charitybot2.storage.repository import Repository
from flask import json
from tests.restters_for_tests import TestFilePath, ServiceTest
from datetime import datetime

donations_db_path = TestFilePath().get_db_path('donations.db')
donations_db_init_script_path = TestFilePath().get_db_path('donations.sql')

status_service = ServiceTest(
    service_name='External API for Performance Tests',
    service_url=api_full_url,
    service_path=external_api_cli_path,
    enter_debug=True,
    extra_args=['--debug'],
    db_path=donations_db_path,
    sql_path=donations_db_init_script_path)

api_v1_base_url = api_full_url + 'api/v1/'
donations_db = Repository(db_path=donations_db_path, debug=True)


def setup_module():
    status_service.start_service()


def teardown_module():
    status_service.stop_service()


def assert_time_taken_in_ms(start_time, maximum_value_ms):
    time_taken = (datetime.now() - start_time).microseconds / 1000
    assert time_taken < maximum_value_ms
    print('Time taken: {} ms Headroom: {} ms'.format(time_taken, maximum_value_ms - time_taken))


class TestEventInfoRetrieval:
    @pytest.mark.skip(reason='Use Locust for performance testing')
    def test_check_path_return_time(self):
        start_time = datetime.now()
        response = requests.get(api_v1_base_url)
        assert_time_taken_in_ms(start_time, 5)
        assert 200 == response.status_code

    def test_retrieve_nominal_event_names(self):
        @pytest.mark.skip(reason='Use Locust for performance testing')
        start_time = datetime.now()
        response = requests.get(api_v1_base_url + 'events')
        assert_time_taken_in_ms(start_time, 5)
        assert 200 == response.status_code
        content = json.loads(response.content)['events']
        assert 1 == len(content)

    @pytest.mark.skip(reason='Use Locust for performance testing')
    def test_retrieve_10_event_names(self):
        # for i in range(0, 10):
        #     donations_db.create_event_table_if_not_exists(event_name='test_{}'.format(i))
        start_time = datetime.now()
        response = requests.get(api_v1_base_url + 'events')
        assert_time_taken_in_ms(start_time, 5)
        assert 200 == response.status_code
        content = json.loads(response.content)['events']
        assert 11 == len(content)  # includes original test table

    @pytest.mark.skip(reason='Use Locust for performance testing')
    def test_retrieve_100_event_names(self):
        # for i in range(11, 100):
        #     donations_db.create_event_table_if_not_exists(event_name='test_{}'.format(i))
        start_time = datetime.now()
        response = requests.get(api_v1_base_url + 'events')
        assert_time_taken_in_ms(start_time, 10)
        assert 200 == response.status_code
        content = json.loads(response.content)['events']
        assert 100 == len(content)

    @pytest.mark.skip(reason='Use Locust for performance testing')
    def test_retrieve_250_event_names(self):
        # for i in range(100, 250):
        #     donations_db.create_event_table_if_not_exists(event_name='test_{}'.format(i))
        start_time = datetime.now()
        response = requests.get(api_v1_base_url + 'events')
        assert_time_taken_in_ms(start_time, 20)
        assert 200 == response.status_code
        content = json.loads(response.content)['events']
        assert 250 == len(content)

    @pytest.mark.skip(reason='Use Locust for performance testing')
    def test_retrieve_1_event_info(self):
        start_time = datetime.now()
        response = requests.get(api_v1_base_url + 'event/test')
        assert_time_taken_in_ms(start_time, 15)
        assert 200 == response.status_code
