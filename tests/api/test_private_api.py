from charitybot2.api_calls.private_api_calls import PrivateApiCalls
from tests.mocks import MockPrivateAPI

mock_private_api = MockPrivateAPI()
private_api_calls = PrivateApiCalls()


def setup_module():
    mock_private_api.start()


def teardown_module():
    mock_private_api.stop()


class TestStartup:
    def test_index_page_returns_200(self):
        response = private_api_calls.get_index()
        assert 200 == response.status_code
