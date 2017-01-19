import time
import requests

from bs4 import BeautifulSoup
from charitybot2.botconfig.event_config import EventConfigurationFromFile
from charitybot2.events.event_loop import EventLoop
from charitybot2.reporter.external_api.external_api import api_full_url
from selenium import webdriver
from tests.integration.test_event_loop_with_mocksite import MockEvent
from tests.mocks import ResetDB, AdjustTestConfig, MockFundraisingWebsite, MockExternalAPI
from tests.paths_for_tests import end_to_end_config_path, repository_db_path, repository_db_script_path

driver = None

config_adjustment = AdjustTestConfig(config_path=end_to_end_config_path)


def get_new_mock_event(end_time_increment=20):
    end_time = int(time.time()) + end_time_increment
    config_adjustment.change_value(key='end_time', value=end_time)
    event_configuration = EventConfigurationFromFile(file_path=end_to_end_config_path).get_event_configuration()
    return MockEvent(
        config_path=end_to_end_config_path,
        mock_name=event_configuration.get_value('internal_name'),
        mock_end_time=end_time)

mock_fundraising_website = MockFundraisingWebsite(fundraiser_name='justgiving')

mock_external_api = MockExternalAPI(extra_args=['--debug'], enter_debug=True)


def setup_module():
    mock_fundraising_website.start()
    mock_external_api.start()
    global driver
    driver = webdriver.Chrome()


def teardown_module():
    mock_fundraising_website.stop()
    mock_external_api.stop()
    global driver
    driver.close()


class TestOverlay:
    overlay_url = api_full_url + 'overlay/{}'

    def test_getting_last_donation_amount_on_overlay(self):
        ResetDB(db_path=repository_db_path, sql_path=repository_db_script_path)
        mock_event = get_new_mock_event()
        mock_fundraising_website.reset_amount()
        print(mock_event.get_currency().get_symbol())
        EventLoop(event=mock_event, debug=True).start()
        response = requests.get(url=self.overlay_url.format(mock_event.get_internal_name()))
        assert 200 == response.status_code
        assert '<!DOCTYPE html>' in response.content.decode('utf-8')
        soup = BeautifulSoup(response.content, 'html.parser')
        amount_raised = soup.find('span', {'id': 'amount_raised'}).text.strip()
        assert '100' == amount_raised
        overlay_text = soup.find('div', {'id': 'overlay-text'}).text.strip().replace('\n', '')
        assert '€100' == overlay_text

    def test_overlay_amount_updates_automagically(self):
        ResetDB(db_path=repository_db_path, sql_path=repository_db_script_path)
        mock_event = get_new_mock_event()
        mock_fundraising_website.reset_amount()
        driver.get(self.overlay_url.format(mock_event.get_internal_name()))
        EventLoop(event=mock_event, debug=True).start()
        soup = BeautifulSoup(driver.find_element_by_id('amount_raised').text.strip(), 'html.parser')
        assert '100' == soup.text
        soup = BeautifulSoup(driver.find_element_by_id('overlay-text').text.strip(), 'html.parser')
        assert '€100' == soup.text
        mock_fundraising_website.increase_amount()
        EventLoop(event=get_new_mock_event(), debug=True).start()
        soup = BeautifulSoup(driver.find_element_by_id('amount_raised').text.strip(), 'html.parser')
        assert '150' == soup.text
        soup = BeautifulSoup(driver.find_element_by_id('overlay-text').text.strip(), 'html.parser')
        assert '€150' == soup.text
