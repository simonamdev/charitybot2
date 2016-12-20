import json

import requests
from charitybot2.paths import external_api_cli_path
from charitybot2.reporter.external_api.external_api import api_full_url
from tests.tests import ServiceTest, TestFilePath

donations_db_path = TestFilePath().get_db_path('donations.db')
donations_db_init_script_path = TestFilePath().get_db_path('donations.sql')


service = ServiceTest(
            service_name='External API for Debug test',
            service_url=api_full_url,
            service_path=external_api_cli_path,
            enter_debug=False,
            extra_args=['--debug'],
            db_path=donations_db_path,
            sql_path=donations_db_init_script_path)


def setup_module():
    service.start_service()


def teardown_module():
    service.stop_service()


class TestExternalAPIDebugState:
    def test_debug_value_changes_when_entering_debug_url(self):
        response = requests.get(api_full_url + 'api/v1/')
        content = json.loads(response.content.decode('utf-8'))
        assert response.status_code == 200
        assert True is content['debug_allowed']
        assert False is content['debug']
        response = requests.get(api_full_url + 'debug')
        content = response.content.decode('utf-8')
        assert response.status_code == 200
        assert 'Entered API debug mode' == content
        response = requests.get(api_full_url + 'api/v1/')
        content = json.loads(response.content.decode('utf-8'))
        assert response.status_code == 200
        assert True is content['debug_allowed']
        assert True is content['debug']
