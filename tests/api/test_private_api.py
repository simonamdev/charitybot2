from charitybot2.api_calls.private_api_calls import PrivateApiCalls
from charitybot2.private_api.private_api import private_api_identity
from tests.mocks import MockPrivateAPI

mock_private_api = MockPrivateAPI()
private_api_calls = PrivateApiCalls()


def setup_module():
    mock_private_api.start()


def teardown_module():
    mock_private_api.stop()


class TestStartup:
    def test_getting_identity_string(self):
        response = private_api_calls.get_index()
        assert isinstance(response['identity'], str)
        assert private_api_identity == response['identity']
        assert isinstance(response['version'], int)
        assert 1 == response['version']
        assert isinstance(response['paths'], dict)
