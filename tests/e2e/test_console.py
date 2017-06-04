from time import sleep

import pytest
from bs4 import BeautifulSoup
from charitybot2.paths import console_script_path, private_api_script_path
from charitybot2.public_api.console.console import app
from charitybot2.sources.url_call import UrlCall
from charitybot2.start_service import Service, ServiceRunner
from tests.setup_test_database import setup_test_database
from selenium import webdriver


driver = None
test_event_identifier = 'test'

console_service = Service(
    name='Test Console',
    app=app,
    address='127.0.0.1',
    port=5000,
    debug=True)
console_service_runner = ServiceRunner(
    service=console_service,
    file_path=console_script_path,
    start_delay=1,
    stop_delay=1)

api_service = Service(
    name='Test Private API',
    app=app,
    address='127.0.0.1',
    port=8001,
    debug=True)
api_service_runner = ServiceRunner(
    service=api_service,
    file_path=private_api_script_path,
    start_delay=1,
    stop_delay=1)


def setup_module():
    setup_test_database()
    console_service_runner.run()
    api_service_runner.run()
    global driver
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)


def teardown_module():
    console_service_runner.stop_running()
    api_service_runner.stop_running()
    global driver
    driver.close()

test_event_url = console_service.full_url + 'event/{}/'.format(test_event_identifier)


class TestConsolePaths:
    @pytest.mark.parametrize('url', [
        console_service.full_url,
        test_event_url
    ])
    def test_paths_return_200(self, url):
        response = UrlCall(url=url).get()
        assert 200 == response.status_code


def get_soup_text_by_id(tag_id):
    global driver
    return BeautifulSoup(driver.find_element_by_id(tag_id).text.strip(), 'html.parser').text


# Helper methods to get data from the page
def get_total_raised():
    driver.get(test_event_url)
    sleep(1)
    total_raised = get_soup_text_by_id('donation-total')
    return total_raised


def get_donation_table_rows():
    driver.get(test_event_url)
    donations_table_body = BeautifulSoup(driver.find_element_by_id('donations-table-body').text.strip(), 'html.parser')
    if donations_table_body == '':
        return []
    return donations_table_body.find_all('tr')


def get_donation_table_row_count():
    return len(get_donation_table_rows())


class TestDonationSubmission:
    @classmethod
    def setup_class(cls):
        setup_test_database(donation_count=0)

    def test_total_is_zero_with_no_rows(self):
        setup_test_database(donation_count=0)
        # make sure there are no rows
        assert 0 == get_donation_table_row_count()
        # make sure the total is 0
        assert '0' == get_total_raised()

    # def test_successful_donation(self):
    #     pass
