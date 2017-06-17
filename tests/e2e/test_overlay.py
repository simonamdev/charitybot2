<<<<<<< HEAD
import time

import pytest
import requests

from bs4 import BeautifulSoup
from charitybot2.botconfig.event_config import EventConfigurationFromFile
from charitybot2.events.event_loop import EventLoop
from charitybot2.reporter.external_api.external_api import api_full_url
from charitybot2.sources.mocks.mocksite import mock_justgiving_fundraising_url, mock_mydonate_teams_url, \
    mock_justgiving_api_url
=======
import random
from time import sleep

from bs4 import BeautifulSoup
from charitybot2.api_calls.private_api_calls import PrivateApiCalls
from charitybot2.models.donation import Donation
from charitybot2.paths import overlay_script_path, private_api_script_path
from charitybot2.private_api.private_api import private_api_service
from charitybot2.public_api.overlay.overlay import app
from charitybot2.start_service import Service, ServiceRunner
>>>>>>> refs/remotes/origin/lavecon-ui
from selenium import webdriver
from tests.integration.test_event_register import get_test_event_configuration
from tests.setup_test_database import setup_test_database
from datetime import datetime

driver = None
test_event_identifier = get_test_event_configuration().identifier

overlay_service = Service(
    name='Test Overlay',
    app=app,
    address='127.0.0.1',
    port=7000,
    debug=True)
overlay_service_runner = ServiceRunner(
    service=overlay_service,
    file_path=overlay_script_path,
    start_delay=3,
    stop_delay=1)

private_api_calls = PrivateApiCalls(base_api_url=private_api_service.full_url)
api_service = Service(
    name='Test Private API',
    app=app,
    address='127.0.0.1',
    port=8001,
    debug=True)
api_service_runner = ServiceRunner(
    service=api_service,
    file_path=private_api_script_path,
    start_delay=2,
    stop_delay=1)

<<<<<<< HEAD
def get_new_mock_event(source_url, end_time_increment=10):
    end_time = int(time.time()) + end_time_increment
    config_adjustment.change_value(key='end_time', value=end_time)
    event_configuration = EventConfigurationFromFile(file_path=end_to_end_config_path).get_event_configuration()
    return MockEvent(
        config_path=end_to_end_config_path,
        mock_name=event_configuration.get_internal_name(),
        mock_end_time=end_time,
        source_url=source_url)

mock_justgiving_fundraising_website = MockFundraisingWebsite(fundraiser_name='justgiving')
mock_mydonate_fundraising_website = MockFundraisingWebsite(fundraiser_name='mydonate')

mock_external_api = MockExternalAPI(extra_args=['--debug'], enter_debug=True)


def setup_module():
    mock_justgiving_fundraising_website.start()
    mock_external_api.start()
=======

def get_soup_text_by_id(tag_id):
    global driver
    return BeautifulSoup(driver.find_element_by_id(tag_id).text.strip(), 'html.parser').text


def setup_module():
    overlay_service_runner.run()
    api_service_runner.run()
>>>>>>> refs/remotes/origin/lavecon-ui
    global driver
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)


def teardown_module():
<<<<<<< HEAD
    mock_justgiving_fundraising_website.stop()
    mock_external_api.stop()
=======
    overlay_service_runner.stop_running()
    api_service_runner.stop_running()
>>>>>>> refs/remotes/origin/lavecon-ui
    global driver
    driver.close()

end_to_end_test_params = [
    (mock_justgiving_fundraising_url, mock_justgiving_fundraising_website),
    (mock_justgiving_api_url,         mock_justgiving_fundraising_website),
    (mock_mydonate_teams_url,         mock_mydonate_fundraising_website)
]


<<<<<<< HEAD
class TestOverlay:
    overlay_url = api_full_url + 'overlay/{}'

    @pytest.mark.parametrize('source_url,mocksite', end_to_end_test_params)
    def test_getting_last_donation_amount_on_overlay(self, source_url, mocksite):
        ResetDB(db_path=repository_db_path, sql_path=repository_db_script_path)
        mock_event = get_new_mock_event(source_url=source_url)
        mocksite.reset_amount()
        EventLoop(event=mock_event, debug=True).start()
        response = requests.get(url=self.overlay_url.format(mock_event.get_internal_name()))
        assert 200 == response.status_code
        assert '<!DOCTYPE html>' in response.content.decode('utf-8')
        soup = BeautifulSoup(response.content, 'html.parser')
        amount_raised = soup.find('span', {'id': 'amount_raised'}).text.strip()
        assert '100' == amount_raised
        overlay_text = soup.find('div', {'id': 'overlay-text'}).text.strip().replace('\n', '')
        assert '€100' == overlay_text

    @pytest.mark.parametrize('source_url,mocksite', end_to_end_test_params)
    def test_overlay_amount_updates_automagically(self, source_url, mocksite):
        ResetDB(db_path=repository_db_path, sql_path=repository_db_script_path)
        mock_event = get_new_mock_event(source_url=source_url)
        mocksite.reset_amount()
        driver.get(self.overlay_url.format(mock_event.get_internal_name()))
        EventLoop(event=mock_event, debug=True).start()
        soup = BeautifulSoup(driver.find_element_by_id('amount_raised').text.strip(), 'html.parser')
        assert '100' == soup.text
        soup = BeautifulSoup(driver.find_element_by_id('overlay-text').text.strip(), 'html.parser')
        assert '€100' == soup.text
        mocksite.increase_amount()
        EventLoop(event=get_new_mock_event(source_url=source_url), debug=True).start()
        soup = BeautifulSoup(driver.find_element_by_id('amount_raised').text.strip(), 'html.parser')
        assert '150' == soup.text
        soup = BeautifulSoup(driver.find_element_by_id('overlay-text').text.strip(), 'html.parser')
        assert '€150' == soup.text
=======
class TestOverlayTotal:
    overlay_total_url = overlay_service.full_url + 'overlay/{}/total'.format(test_event_identifier)

    @classmethod
    def setup_class(cls):
        setup_test_database(donation_count=0)

    def test_overlay_total_is_as_expected(self):
        # since no donations are added, it *should* be €0
        driver.get(self.overlay_total_url)
        total_amount = get_soup_text_by_id('overlay-text')
        sleep(2)
        assert '€0' == total_amount

    def test_overlay_total_increases_when_donation_is_added(self):
        driver.get(self.overlay_total_url)
        donation = Donation(amount=5.5, event_identifier=test_event_identifier)
        private_api_calls.register_donation(donation=donation)
        sleep(5)
        total_amount = get_soup_text_by_id('overlay-text')
        assert '€5.5' == total_amount


class TestOverlayTicker:
    overlay_ticker_url = overlay_service.full_url + 'overlay/{}/ticker'.format(test_event_identifier)

    @classmethod
    def setup_class(cls):
        setup_test_database(donation_count=0)

    @staticmethod
    def get_table_rows():
        global driver
        rows = driver.find_elements_by_tag_name('tr')
        soup = []
        for row in rows:
            parsed_soup = BeautifulSoup(row.text, 'html.parser').text.split(' ')
            soup.append(dict(timestamp=parsed_soup[0], amount=parsed_soup[1]))
        return soup

    def test_overlay_update(self):
        driver.get(self.overlay_ticker_url)
        rows = self.get_table_rows()
        # Header row only
        assert 1 == len(rows)
        donation = Donation(amount=5.5, event_identifier=test_event_identifier)
        private_api_calls.register_donation(donation=donation)
        sleep(4)
        rows = self.get_table_rows()
        assert 2 == len(rows)

    def test_overlay_updating_does_not_exceed_default_limit(self):
        setup_test_database(donation_count=0)
        driver.get(self.overlay_ticker_url)
        rows = self.get_table_rows()
        # Header row only
        assert 1 == len(rows)
        amount_added = 15
        for i in range(0, amount_added):
            donation = Donation(amount=random.uniform(1.0, 10.0), event_identifier=test_event_identifier)
            private_api_calls.register_donation(donation=donation)
        sleep(3)
        rows = self.get_table_rows()
        assert 11 == len(rows)


class TestOverlayLatestDonation:
    overlay_latest_url = overlay_service.full_url + 'overlay/{}/latest'.format(test_event_identifier)

    @staticmethod
    def setup_method():
        setup_test_database(donation_count=0)

    @staticmethod
    def get_latest_donation():
        return get_soup_text_by_id('overlay-latest')

    def test_overlay_latest_with_no_donations_returns_error(self):
        driver.get(self.overlay_latest_url)
        latest_donation = self.get_latest_donation()
        assert '' == latest_donation

    def test_overlay_latest_with_one_donation(self):
        driver.get(self.overlay_latest_url)
        donation = Donation(
            amount=5,
            event_identifier=test_event_identifier,
            timestamp=5,
            donor_name='donor')
        private_api_calls.register_donation(donation=donation)
        sleep(2)
        latest_donation = self.get_latest_donation()
        # €5 from DONOR at TIME
        split = latest_donation.split(' ')
        amount = int(split[0].replace('€', ''))
        donor = split[2]
        # timestamp = split[4]
        assert 5 == amount
        assert 'donor' == donor.replace(',', '')
        # assert 5 == int(timestamp)

    def test_overlay_latest_with_several_donations(self):
        driver.get(self.overlay_latest_url)
        test_amount = 10
        for i in range(1, test_amount + 1):
            donation = Donation(
                amount=i,
                event_identifier=test_event_identifier,
                timestamp=i,
                donor_name='donor')
            private_api_calls.register_donation(donation=donation)
        sleep(2)
        latest_donation = self.get_latest_donation()
        # €amount from DONOR at TIME
        split = latest_donation.split(' ')
        amount = int(split[0].replace('€', ''))
        donor = split[2]
        # timestamp = split[4]
        assert test_amount == amount
        assert 'donor' == donor.replace(',', '')
        # assert test_amount == int(timestamp)
>>>>>>> refs/remotes/origin/lavecon-ui
