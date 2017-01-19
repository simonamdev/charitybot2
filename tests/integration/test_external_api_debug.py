import json

import requests
from charitybot2.reporter.external_api.external_api import api_full_url
from tests.mocks import MockExternalAPI

mock_external_api = MockExternalAPI(extra_args=['--debug'], enter_debug=False)


def setup_module():
    mock_external_api.start()


def teardown_module():
    mock_external_api.stop()


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
