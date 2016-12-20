import requests
from bs4 import BeautifulSoup
from charitybot2.paths import external_api_cli_path
from charitybot2.reporter.external_api.external_api import api_full_url, api_paths
from flask import json
from tests.tests import TestFilePath, ServiceTest

donations_db_path = TestFilePath().get_db_path('donations.db')
donations_db_init_script_path = TestFilePath().get_db_path('donations.sql')

status_service = ServiceTest(
    service_name='External API',
    service_url=api_full_url,
    service_path=external_api_cli_path,
    enter_debug=True,
    extra_args=['--debug'],
    db_path=donations_db_path,
    sql_path=donations_db_init_script_path)

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
        assert ['test'] == content

    def test_getting_nonexistent_event_returns_404(self):
        response = requests.get(api_v1_base_url + 'event/bla')
        content = json.loads(response.content)
        assert 404 == response.status_code
        assert content['error'] == 'Not found'

    def test_getting_event_info(self):
        response = requests.get(api_v1_base_url + 'event/test')
        content = json.loads(response.content)
        assert 200 == response.status_code
        assert isinstance(content, dict)
        assert 'test' == content['name']
        assert 15 == content['donation_count']
        assert 13.92 == content['donation_average']
        assert 42.0 == content['largest_donation']
        assert '£' == content['currency_symbol']
        assert 0 == content['last_hour_donation_count']  # technically doesn't test if it works
        assert 0 == content['start_time']
        assert 9999999999 == content['end_time']


class TestDonationsGET:
    def test_getting_donations_of_non_existent_event_returns_404(self):
        response = requests.get(api_v1_base_url + 'event/bla/donations')
        assert 404 == response.status_code
        response = requests.get(api_v1_base_url + 'event/bla/donations/last')
        assert 404 == response.status_code

    def test_get_donation_data(self):
        response = requests.get(api_v1_base_url + 'event/test/donations')
        content = json.loads(response.content)['donations']
        assert 200 == response.status_code
        assert isinstance(content, list)
        assert 11.45 == content[0]['amount']
        assert 33.2 == content[0]['total_raised']

    def test_getting_donation_data_with_limit(self):
        response = requests.get(api_v1_base_url + 'event/test/donations?limit=2')
        content = json.loads(response.content)['donations']
        assert 200 == response.status_code
        assert 2 == len(content)

    def test_getting_last_donation_only(self):
        response = requests.get(api_v1_base_url + 'event/test/donations/last')
        content = json.loads(response.content)
        assert 200 == response.status_code
        assert 8.5 == content['amount']
        assert 230.5 == content['total_raised']

    def test_getting_donations_distribution(self):
        response = requests.get(api_v1_base_url + 'event/test/donations/distribution')
        assert 200 == response.status_code
        content = json.loads(response.content)['donations_distribution']
        assert isinstance(content, dict)
        expected_distribution = {
            '0-9': 8,
            '10-19': 2,
            '20-29': 2,
            '30-39': 2,
            '40-49': 1,
            '50-75': 0,
            '76-99': 0,
            '100-10000': 0
        }
        assert expected_distribution == content


class TestStatsConsoleGET:
    def test_stats_console_returns_200(self):
        response = requests.get(api_full_url + 'stats/test')
        assert 200 == response.status_code

    def test_accessing_status_console_of_non_existent_event_returns_404(self):
        response = requests.get(api_v1_base_url + 'event/foobar/status')
        assert 404 == response.status_code


class TestOverlayGET:
    def test_get_amount_raised_for_overlay(self):
        response = requests.get(api_full_url + 'overlay/test')
        assert 200 == response.status_code
        assert '<!DOCTYPE html>' in response.content.decode('utf-8')
        soup = BeautifulSoup(response.content, 'html.parser')
        amount_raised = soup.find('span', {'id': 'amount_raised'}).text.strip()
        assert '230' == amount_raised