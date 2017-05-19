import pytest
from charitybot2.paths import console_script_path
from charitybot2.public_api.console.console import app
from charitybot2.sources.url_call import UrlCall
from charitybot2.start_service import Service, ServiceRunner
from tests.setup_test_database import setup_test_database

test_event_identifier = 'test'
service = Service(
    name='Test Private API',
    app=app,
    address='127.0.0.1',
    port=5000,
    debug=True)
service_runner = ServiceRunner(service=service, file_path=console_script_path)


def setup_module():
    setup_test_database()
    service_runner.run()


def teardown_module():
    service_runner.stop_running()


class TestConsolePaths:
    @pytest.mark.parametrize('url', [
        service.full_url,
        service.full_url + 'event/{}/'.format(test_event_identifier),
    ])
    def test_paths_return_200(self, url):
        response = UrlCall(url=url).get()
        assert 200 == response.status_code
