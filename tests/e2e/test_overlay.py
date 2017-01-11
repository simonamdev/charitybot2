import time
import requests

from bs4 import BeautifulSoup
from charitybot2.events.event_loop import EventLoop
from charitybot2.paths import mocksite_path, external_api_cli_path
from charitybot2.reporter.external_api.external_api import api_full_url
from charitybot2.sources.mocks.mocksite import mocksite_full_url
from selenium import webdriver
from tests.integration.test_event_loop_with_mocksite import MockEvent
from tests.tests import ServiceTest, TestFilePath, ResetDB, AdjustTestConfig

driver = None

donations_db_path = TestFilePath().get_db_path('donations.db')
donations_db_init_script_path = TestFilePath().get_db_path('donations.sql')
config_adjustment = AdjustTestConfig(config_path=TestFilePath().get_config_path('event', 'E2E_Test_Charity_Event.json'))
event_name = 'E2E_Test_Charity_Event'

mocksite = ServiceTest(
    service_name='Donations Mocksite',
    service_url=MockEvent.mocksite_base_url,
    service_path=mocksite_path,
    enter_debug=False)


external_api = ServiceTest(
    service_name='External API',
    service_url=api_full_url,
    service_path=external_api_cli_path,
    enter_debug=True,
    extra_args=['--debug'])


def reset_mocksite():
    r = requests.get(url=mocksite_full_url + 'reset')
    assert 200 == r.status_code


def setup_module():
    mocksite.start_service()
    external_api.start_service()
    global driver
    driver = webdriver.Chrome()


def teardown_module():
    mocksite.stop_service()
    external_api.stop_service()
    global driver
    driver.close()


class TestOverlay:
    overlay_url = api_full_url + 'overlay/{}'

    def test_getting_last_donation_amount_on_overlay(self):
        ResetDB(db_path=donations_db_path, sql_path=donations_db_init_script_path)
        config_adjustment.change_value(key='end_time', value=int(time.time()) + 20)
        reset_mocksite()
        time.sleep(2)
        EventLoop(event=MockEvent(event_name, int(time.time()) + 10), debug=True).start()
        response = requests.get(url=self.overlay_url.format(event_name))
        assert 200 == response.status_code
        assert '<!DOCTYPE html>' in response.content.decode('utf-8')
        soup = BeautifulSoup(response.content, 'html.parser')
        amount_raised = soup.find('span', {'id': 'amount_raised'}).text.strip()
        assert '100' == amount_raised
        overlay_text = soup.find('div', {'id': 'overlay-text'}).text.strip().replace('\n', '')
        print(overlay_text)
        assert '£100' == overlay_text

    def test_overlay_amount_updates_automagically(self):
        ResetDB(db_path=donations_db_path, sql_path=donations_db_init_script_path)
        config_adjustment.change_value(key='end_time', value=int(time.time()) + 25)
        reset_mocksite()
        time.sleep(2)
        driver.get(self.overlay_url.format(event_name))
        EventLoop(event=MockEvent(event_name, int(time.time()) + 10), debug=True).start()
        soup = BeautifulSoup(driver.find_element_by_id('amount_raised').text.strip(), 'html.parser')
        assert '100' == soup.text
        soup = BeautifulSoup(driver.find_element_by_id('overlay-text').text.strip(), 'html.parser')
        assert '£100' == soup.text
        # refactor this following line later when separating mocksite logic from mockevent object
        requests.get(url=MockEvent.mocksite_base_url + 'justgiving/increase/')
        EventLoop(event=MockEvent(event_name, int(time.time()) + 10), debug=True).start()
        soup = BeautifulSoup(driver.find_element_by_id('amount_raised').text.strip(), 'html.parser')
        assert '150' == soup.text
        soup = BeautifulSoup(driver.find_element_by_id('overlay-text').text.strip(), 'html.parser')
        assert '£150' == soup.text
