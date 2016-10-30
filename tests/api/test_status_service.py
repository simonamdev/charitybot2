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


def setup_module():
    status_service.start_service()


def teardown_module():
    status_service.stop_service()


class TestServiceBasicResponses:
    def test_index_page_returns_service_name(self):
        response = requests.get(service_full_url + 'identity')
        assert 200 == response.status_code
        assert b'Status Service' == response.content

    def test_event_name_comes_up_on_index_page(self):
        response = requests.get(service_full_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        event_name_div = soup.find('div', {'id': 'event_names'})
        names = event_name_div.find_all('li')
        assert len(names) == 1
        assert 'test' == names[0].text
