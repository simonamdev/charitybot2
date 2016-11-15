import time
import requests

from bs4 import BeautifulSoup
from charitybot2.events.event_loop import EventLoop
from charitybot2.paths import mocksite_path, external_api_path
from charitybot2.reporter.external_api.external_api import api_full_url
from charitybot2.sources.mocks.mocksite import mocksite_full_url
from selenium import webdriver
from tests.integration.test_event_loop_with_mocksite import MockEvent
from tests.tests import ServiceTest, TestFilePath

driver = None

donations_db_path = TestFilePath().get_db_path('donations.db')
donations_db_init_script_path = TestFilePath().get_db_path('donations.sql')

mocksite = ServiceTest(
    service_name='Donations Mocksite',
    service_url=MockEvent.mocksite_base_url,
    service_path=mocksite_path,
    enter_debug=False)


external_api = ServiceTest(
    service_name='External_API',
    service_url=api_full_url,
    service_path=external_api_path,
    db_path=donations_db_path,
    sql_path=donations_db_init_script_path,
    enter_debug=True)


def reset_mocksite():
    r = requests.get(url=mocksite_full_url + 'reset')
    assert 200 == r.status_code


def setup_module():
    global driver
    driver = webdriver.Chrome()
    mocksite.start_service()
    external_api.start_service()


def teardown_module():
    mocksite.stop_service()
    external_api.stop_service()
    global driver
    driver.close()


class TestOverlay:
    overlay_url = api_full_url + 'event/{}/overlay'

    def test_getting_last_donation_amount_on_overlay(self):
        reset_mocksite()
        time.sleep(2)
        event_name = 'test'
        test_event = MockEvent(event_name, time.time() + 10)
        test_event_loop = EventLoop(event=test_event, debug=True)
        test_event_loop.start()
        response = requests.get(url=self.overlay_url.format(event_name))
        assert 200 == response.status_code
        assert '<!DOCTYPE html>' in response.content.decode('utf-8')
        soup = BeautifulSoup(response.content, 'html.parser')
        amount_raised = soup.find('span', {'id': 'amount_raised'}).text.strip()
        assert '250.52' == amount_raised

    def test_overlay_amount_updates_automagically(self):
        reset_mocksite()
        time.sleep(2)
        event_name = 'test_two'
        driver.get(self.overlay_url.format(event_name))
        test_event = MockEvent(event_name, time.time() + 25)
        test_event_loop = EventLoop(event=test_event, debug=True)
        test_event_loop.start()
        soup = BeautifulSoup(driver.find_element_by_id('amount_raised').text.strip(), 'html.parser')
        assert '400.52' == soup.text
