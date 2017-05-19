import pytest
from charitybot2.public_api.console.console import console_full_url
from charitybot2.sources.url_call import UrlCall
from tests.mocks import MockConsole
from tests.setup_test_database import setup_test_database

mock_console = MockConsole()
test_event_identifier = 'test'


def setup_module():
    setup_test_database()
    mock_console.start()


def teardown_module():
    mock_console.stop()


class TestConsolePaths:
    @pytest.mark.parametrize('url', [
        console_full_url,
        console_full_url + 'event/{}/'.format(test_event_identifier),
    ])
    def test_paths_return_200(self, url):
        response = UrlCall(url=url).get()
        assert 200 == response.status_code
