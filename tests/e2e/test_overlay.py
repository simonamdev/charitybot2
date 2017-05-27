from time import sleep

from bs4 import BeautifulSoup
from charitybot2.api_calls.private_api_calls import PrivateApiCalls
from charitybot2.models.donation import Donation
from charitybot2.paths import overlay_script_path, private_api_script_path
from charitybot2.private_api.private_api import private_api_service
from charitybot2.public_api.overlay.overlay import app
from charitybot2.start_service import Service, ServiceRunner
from selenium import webdriver
from tests.integration.test_event_register import get_test_event_configuration
from tests.setup_test_database import setup_test_database

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


def get_soup_text_by_id(tag_id):
    global driver
    return BeautifulSoup(driver.find_element_by_id(tag_id).text.strip(), 'html.parser').text


def setup_module():
    overlay_service_runner.run()
    api_service_runner.run()
    global driver
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)


def teardown_module():
    overlay_service_runner.stop_running()
    api_service_runner.stop_running()
    global driver
    driver.close()


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

    def test_overlay_ticker_has_rows_as_many_as_limit(self):
        driver.get(self.overlay_ticker_url)
        rows = self.get_table_rows()
        # Header row only
        assert 1 == len(rows)
        donation = Donation(amount=5.5, event_identifier=test_event_identifier)
        private_api_calls.register_donation(donation=donation)
        sleep(4)
        rows = self.get_table_rows()
        assert 2 == len(rows)
