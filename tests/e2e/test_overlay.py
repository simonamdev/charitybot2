from charitybot2.api_calls.private_api_calls import PrivateApiCalls
from charitybot2.paths import overlay_script_path, private_api_script_path
from charitybot2.private_api.private_api import private_api_service
from charitybot2.public_api.overlay.overlay import app
from charitybot2.start_service import Service, ServiceRunner
from tests.integration.test_event_register import get_test_event_configuration
from tests.setup_test_database import setup_test_database

driver = None

service = Service(
    name='Test Overlay',
    app=app,
    address='127.0.0.1',
    port=7000,
    debug=True)
overlay_service_runner = ServiceRunner(service=service, file_path=overlay_script_path)

private_api_calls = PrivateApiCalls(base_api_url=private_api_service.full_url)
test_event_identifier = get_test_event_configuration().identifier
service = Service(
    name='Test Private API',
    app=app,
    address='127.0.0.1',
    port=8001,
    debug=True)
api_service_runner = ServiceRunner(service=service, file_path=private_api_script_path)


def setup_module():
    setup_test_database(donation_count=10)
    overlay_service_runner.run()
    api_service_runner.run()


def teardown_module():
    overlay_service_runner.stop_running()
    api_service_runner.stop_running()


class TestOverlay:
    def test_overlay_value_is_as_expected(self):
        pass

    def test_overlay_value_increases_when_donation_is_added(self):
        pass
