import requests
from bs4 import BeautifulSoup
from charitybot2.paths import external_api_path
from charitybot2.reporter.external_api.external_api import api_full_url
from flask import json
from tests.tests import TestFilePath, ServiceTest

donations_db_path = TestFilePath().get_db_path('donations.db')
donations_db_init_script_path = TestFilePath().get_db_path('donations.sql')

status_service = ServiceTest(
    service_name='External API',
    service_url=api_full_url,
    service_path=external_api_path,
    enter_debug=True,
    db_path=donations_db_path,
    sql_path=donations_db_init_script_path)


def setup_module():
    status_service.start_service()


def teardown_module():
    status_service.stop_service()


paths = ['events']


class TestGET:
    def test_index_route_returns_information_object(self):
        response = requests.get(api_full_url)
        content = json.loads(response.content)
        assert 200 == response.status_code
        assert isinstance(content['paths'], list)

    def test_information_object_contains_all_paths(self):
        response = requests.get(api_full_url)
        content = json.loads(response.content)
        assert sorted(paths) == sorted(content['paths'])

    def test_events_route_returns_event_names(self):
        response = requests.get(api_full_url + 'events')
        content = json.loads(response.content)['events']
        assert ['test'] == content

    def test_getting_nonexistent_event_returns_404(self):
        response = requests.get(api_full_url + 'event/bla')
        content = json.loads(response.content)
        assert 404 == response.status_code
        assert content['error'] == 'Not found'

    def test_getting_event_info(self):
        response = requests.get(api_full_url + 'event/test')
        content = json.loads(response.content)
        assert 200 == response.status_code
        assert isinstance(content, dict)
        assert 'test' == content['name']
        assert 15 == content['donation_count']
        assert 13.92 == content['donation_average']
        assert 42.0 == content['largest_donation']
        assert '£' == content['currency_symbol']

    def test_getting_donations_of_non_existent_event_returns_404(self):
        response = requests.get(api_full_url + 'event/bla/donations')
        assert 404 == response.status_code

    def test_get_donation_data(self):
        response = requests.get(api_full_url + 'event/test/donations')
        content = json.loads(response.content)['donations']
        assert 200 == response.status_code
        assert isinstance(content, list)
        assert 11.45 == content[0]['amount']
        assert 33.2 == content[0]['total_raised']

    def test_getting_donation_data_with_limit(self):
        response = requests.get(api_full_url + 'event/test/donations?limit=2')
        content = json.loads(response.content)['donations']
        assert 200 == response.status_code
        assert 2 == len(content)

    def test_get_amount_raised_for_overlay(self):
        response = requests.get(api_full_url + 'event/test/overlay')
        assert 200 == response.status_code
        assert '<!DOCTYPE html>' in response.content.decode('utf-8')
        soup = BeautifulSoup(response.content, 'html.parser')
        amount_raised = soup.find('span', {'id': 'amount_raised'}).text.strip()
        assert '£230.5' == amount_raised
