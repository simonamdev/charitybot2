import random
from time import sleep

import pytest
from bs4 import BeautifulSoup
from charitybot2.api_calls.private_api_calls import PrivateApiCalls
from charitybot2.models.donation import Donation
from charitybot2.paths import console_script_path, private_api_script_path
from charitybot2.private_api.private_api import private_api_service
from charitybot2.public_api.console.console import app
from charitybot2.sources.url_call import UrlCall
from charitybot2.start_service import Service, ServiceRunner
from tests.setup_test_database import setup_test_database
from selenium import webdriver


driver = None
test_event_identifier = 'test'
private_api_calls = PrivateApiCalls(base_api_url=private_api_service.full_url)


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
    # setup_test_database()
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
    sleep(2)
    donations_table_body = driver.find_element_by_id('donations-table-body')
    donations_table_body_text = BeautifulSoup(donations_table_body.text.strip(), 'html.parser')
    if donations_table_body_text == '':
        return []
    table_rows = donations_table_body.find_elements_by_tag_name('tr')
    return [convert_web_element_to_donation_dict(row) for row in table_rows]


def convert_web_element_to_donation_dict(web_element):
    # break up the tr into separate tds
    row_tds = web_element.find_elements_by_tag_name('td')
    return dict(
        amount=row_tds[1].text,
        timestamp=row_tds[2].text,
        donor=row_tds[3].text,
        notes=row_tds[4].text,
        external_reference=row_tds[5].text,
        internal_reference=row_tds[6].text)


def get_donation_table_row_count():
    return len(get_donation_table_rows())


class TestDonationSubmission:
    def test_total_is_zero_with_no_rows(self):
        setup_test_database(donation_count=0)
        # make sure there are no rows
        assert 0 == get_donation_table_row_count()
        # make sure the total is 0
        assert '0' == get_total_raised()

    def test_donation_from_api(self):
        setup_test_database(donation_count=0)
        test_amount = random.uniform(1.5, 50.3)
        donation = Donation(amount=test_amount, event_identifier=test_event_identifier)
        private_api_calls.register_donation(donation=donation)
        rows = get_donation_table_rows()
        assert 1 == len(rows)
        donation_row = rows[0]
        assert round(test_amount, 2) == float(donation_row['amount'].replace('€', ''))

    # def test_successful_donation(self):
    #     pass
