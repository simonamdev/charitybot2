from charitybot2.api.donations_api import donations_api, app, donations_api_identity
from charitybot2.api_calls.donations_api_wrapper import DonationsApiWrapper
from charitybot2.paths import donation_api_path
from charitybot2.start_service import Service, ServiceRunner
from helpers.event_config import get_test_event_configuration
from helpers.setup_test_database import setup_test_database

donations_api_wrapper = DonationsApiWrapper(base_url=donations_api.full_url)
test_event_identifier = get_test_event_configuration().identifier

service = Service(
    name='Donations Service',
    app=app,
    address='127.0.0.1',
    port=8001,
    debug=True)
service_runner = ServiceRunner(service=service, file_path=donation_api_path)


def setup_module():
    setup_test_database(donation_count=10)
    service_runner.run()


def teardown_module():
    service_runner.stop_running()


class TestStartup:
    def test_getting_identity(self):
        response = donations_api_wrapper.get_index()
        assert isinstance(response['identity'], str)
        assert donations_api_identity == response['identity']
        assert isinstance(response['version'], int)
        assert 1 == response['version']
        assert True is response['debug']

