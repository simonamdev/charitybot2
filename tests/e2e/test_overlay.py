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
    start_delay=1,
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
    global driver
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    setup_test_database(donation_count=0)
    overlay_service_runner.run()
    api_service_runner.run()


def teardown_module():
    global driver
    driver.close()
    overlay_service_runner.stop_running()
    api_service_runner.stop_running()


class TestOverlay:
    overlay_total_url = overlay_service.full_url + 'overlay/{}/total'.format(test_event_identifier)

    def test_overlay_total_is_as_expected(self):
        # since no donations are added, it *should* be €0
        driver.get(self.overlay_total_url)
        total_amount = get_soup_text_by_id('overlay-total')
        assert '€0' == total_amount

    def test_overlay_total_increases_when_donation_is_added(self):
        driver.get(self.overlay_total_url)
        donation = Donation(amount=5.0, event_identifier=test_event_identifier)
        private_api_calls.register_donation(donation=donation)
        from time import sleep
        sleep(5)
        total_amount = get_soup_text_by_id('overlay-total')
        assert '€5.0' == total_amount
