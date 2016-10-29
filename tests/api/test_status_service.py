import requests
from charitybot2.paths import status_service_path
from charitybot2.reporter.status_service.status_service import service_full_url
from tests.tests import TestFilePath, ServiceTest

donations_db_path = TestFilePath().get_db_path('donations.db')
donations_db_init_script_path = TestFilePath().get_db_path('donations.sql')

status_service = ServiceTest(
    service_name='Status Service',
    service_url=service_full_url,
    service_path=status_service_path,
    db_path=donations_db_path,
    sql_path=donations_db_init_script_path)


def setup_module():
    status_service.start_service()


def teardown_module():
    status_service.stop_service()


class TestServiceBasicResponses:
    def test_index_page_returns_service_name(self):
        response = requests.get(service_full_url)
        assert 200 == response.status_code
        assert b'Status Service' == response.content
