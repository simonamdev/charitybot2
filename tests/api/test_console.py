from charitybot2.public_api.console.console import console_full_url
from charitybot2.sources.url_call import UrlCall
from tests.mocks import MockConsole

mock_console = MockConsole()


def setup_module():
    mock_console.start()


def teardown_module():
    mock_console.stop()


class TestConsolePaths:
    def test_index_page_returns_200(self):
        url = console_full_url
        response = UrlCall(url=url).get()
        assert 200 == response.status_code
