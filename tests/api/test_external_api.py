import copy

import requests
from bs4 import BeautifulSoup
from charitybot2.paths import external_api_cli_path
from charitybot2.reporter.external_api.external_api import api_full_url, api_paths
from flask import json
from tests.restters_for_tests import TestFilePath, ServiceTest
from tests.unit.test_repository import event_names

db_path = TestFilePath().get_repository_db_path()
db_script_path = TestFilePath().get_repository_script_path()

status_service = ServiceTest(
    service_name='External API',
    service_url=api_full_url,
    service_path=external_api_cli_path,
    enter_debug=True,
    extra_args=['--debug'],
    db_path=db_path,
    sql_path=db_script_path)

api_v1_base_url = api_full_url + 'api/v1/'


def setup_module():
    status_service.start_service()


def teardown_module():
    status_service.stop_service()


class TestEventGET:
    def test_index_route_returns_paths(self):
        response = requests.get(api_v1_base_url)
        content = json.loads(response.content)
        assert 200 == response.status_code
        assert isinstance(content['paths'], dict)
        assert sorted(api_paths) == sorted(content['paths'])

    def test_events_route_returns_event_names(self):
        response = requests.get(api_v1_base_url + 'events')
        content = json.loads(response.content)['events']
        print(content)
        assert ['TestOne', 'TestTwo', 'TestThree', 'TestFour', 'NoDonations', 'LastOneInvalid', 'OnlyInvalid'] == content

    def test_getting_nonexistent_event_returns_404(self):
        response = requests.get(api_v1_base_url + 'event/bla')
        content = json.loads(response.content)
        assert 404 == response.status_code
        assert content['error'] == 'Not found'

    def test_getting_event_info(self):
        response = requests.get(api_v1_base_url + 'event/TestOne')
        content = json.loads(response.content)
        assert 200 == response.status_code
        assert isinstance(content, dict)
        assert 'TestOne' == content['name']
        assert '£' == content['currency_symbol']
        assert 1477256983 == content['start_time']
        assert 1477256985 == content['end_time']
        assert 100.0 == content['amount_raised']
        assert 1000 == content['target_amount']


class TestDonationsGET:
    def test_getting_donations_of_non_existent_event_returns_404(self):
        response = requests.get(api_v1_base_url + 'event/bla/donations')
        assert 404 == response.status_code
        response = requests.get(api_v1_base_url + 'event/bla/donations/last')
        assert 404 == response.status_code

    def test_getting_donations_info(self):
        response = requests.get(api_v1_base_url + 'event/TestOne/donations/info')
        content = json.loads(response.content.decode('utf-8'))['donations_info']
        assert 200 == response.status_code
        assert isinstance(content, dict)
        assert 5 == content['count']
        assert 20 == content['average']
        assert isinstance(content['largest'], dict)
        assert 63.17 == content['largest']['amount']
        assert 1477257000 == content['largest']['timestamp']
        assert isinstance(content['last'], dict)
        assert 63.17 == content['last']['amount']
        assert 1477257000 == content['last']['timestamp']
        assert isinstance(content['specific'], dict)
        assert 0 == content['specific']['count']
        assert 3600 == content['specific']['timespan']

    def test_get_donation_data(self):
        response = requests.get(api_v1_base_url + 'event/TestOne/donations')
        content = json.loads(response.content)['donations']
        assert 200 == response.status_code
        assert isinstance(content, list)
        assert 10.5 == content[1]['amount']
        assert 21.0 == content[1]['total_raised']

    def test_getting_donation_data_with_limit(self):
        response = requests.get(api_v1_base_url + 'event/TestOne/donations?limit=2')
        content = json.loads(response.content)['donations']
        assert 200 == response.status_code
        assert 2 == len(content)

    def test_getting_last_donation_only(self):
        response = requests.get(api_v1_base_url + 'event/TestOne/donations/last')
        content = json.loads(response.content)
        assert 200 == response.status_code
        assert 63.17 == content['amount']
        assert 100.0 == content['total_raised']

    def test_getting_donations_distribution(self):
        response = requests.get(api_v1_base_url + 'event/TestOne/donations/distribution')
        assert 200 == response.status_code
        content = json.loads(response.content)['donations_distribution']
        assert isinstance(content, dict)
        expected_distribution = {
            '0-9': 1,
            '10-19': 3,
            '20-29': 0,
            '30-39': 0,
            '40-49': 0,
            '50-75': 1,
            '76-99': 0,
            '100-10000': 0
        }
        assert expected_distribution == content


class TestStatsConsoleGET:
    def test_stats_console_returns_200(self):
        response = requests.get(api_full_url + 'stats/TestOne')
        assert 200 == response.status_code

    def test_every_event_stats_console_returns_200(self):
        events = list(copy.deepcopy(event_names))
        events.remove('valid_configured_event')
        for event in events:
            url = api_full_url + 'stats/' + event
            response = requests.get(url)
            assert 200 == response.status_code

    def test_accessing_status_console_of_non_existent_event_returns_404(self):
        response = requests.get(api_v1_base_url + 'event/foobar/status')
        assert 404 == response.status_code


class TestOverlayGET:
    def test_get_amount_raised_for_overlay(self):
        response = requests.get(api_full_url + 'overlay/TestOne')
        assert 200 == response.status_code
        assert '<!DOCTYPE html>' in response.content.decode('utf-8')
        soup = BeautifulSoup(response.content, 'html.parser')
        amount_raised = soup.find('span', {'id': 'amount_raised'}).text.strip()
        assert '100' == amount_raised

    def test_get_overlay_for_non_existent_event_returns_three_dots(self):
        response = requests.get(api_full_url + 'overlay/blablablalba')
        assert 200 == response.status_code
        assert '<!DOCTYPE html>' in response.content.decode('utf-8')
        soup = BeautifulSoup(response.content, 'html.parser')
        amount_raised = soup.find('span', {'id': 'amount_raised'}).text.strip()
        assert '...' == amount_raised
