import requests
from charitybot2.paths import status_service_path
from charitybot2.reporter.status_service.status_service import service_full_url
from tests.tests import TestFilePath, ServiceTest
from bs4 import BeautifulSoup

donations_db_path = TestFilePath().get_db_path('donations.db')
donations_db_init_script_path = TestFilePath().get_db_path('donations.sql')

status_service = ServiceTest(
    service_name='Status Service',
    service_url=service_full_url,
    service_path=status_service_path,
    enter_debug=True,
    db_path=donations_db_path,
    sql_path=donations_db_init_script_path)


def get_tag_soup(url, tag_type, tag_params):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.find(tag_type, tag_params)


def setup_module():
    status_service.start_service()


def teardown_module():
    status_service.stop_service()


class TestServiceBasicResponses:
    def test_index_page_returns_service_name(self):
        response = requests.get(service_full_url + 'identity')
        assert 200 == response.status_code
        assert b'Status Service' == response.content


class TestIndexPageContents:
    def test_event_name_comes_up_on_index_page(self):
        names = get_tag_soup(service_full_url, 'div', {'id': 'event_names'}).find_all('li')
        assert len(names) == 1
        assert 'test' == names[0].text


class TestEventPageContents:
    event_page_url = service_full_url + 'event/test'

    def test_event_name_is_in_header(self):
        event_name = get_tag_soup(self.event_page_url, 'h1', {'id': 'event_name'})
        assert 'test' == event_name.text.strip()

    def test_donation_count_is_correct(self):
        donation_count = get_tag_soup(self.event_page_url, 'span', {'id': 'donation_count'})
        assert 15 == int(donation_count.text.strip())

    def test_donation_average_is_correct(self):
        donation_average = get_tag_soup(self.event_page_url, 'span', {'id': 'donation_average'})
        assert 13.92 == round(float(donation_average.text.strip()), 2)

    def test_largest_donation_amount_is_correct(self):
        donation_maximum = get_tag_soup(self.event_page_url, 'span', {'id': 'largest_donation'})
        assert 42.0 == round(float(donation_maximum.text.strip()), 2)
