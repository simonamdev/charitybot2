from charitybot2.api.events_api import events_api, app, events_api_identity, port
from charitybot2.api_calls.events_api_wrapper import EventsApiWrapper
from charitybot2.paths import events_api_path, test_repository_db_path
from charitybot2.start_service import Service, ServiceRunner
from helpers.event_config import get_test_event_configuration
from helpers.setup_test_database import setup_test_database, register_test_event, wipe_database

events_api_wrapper = EventsApiWrapper(base_url=events_api.full_url)
test_event_identifier = get_test_event_configuration().identifier

service = Service(
    name='Events Service',
    app=app,
    address='127.0.0.1',
    port=port,
    debug=True)
service_runner = ServiceRunner(service=service, file_path=events_api_path)

default_number_of_test_events = 3
test_events = []


def setup_test_events(count=default_number_of_test_events):
    wipe_database(test_repository_db_path)
    test_internal_reference_string = 'test_event_{}'
    event_configurations = []
    for i in range(0, count):
        updated_values = {
            'identifier': test_internal_reference_string.format(i)
        }
        event_configuration = get_test_event_configuration(updated_values=updated_values)
        register_test_event(test_repository_db_path, event_configuration=event_configuration)
        event_configurations.append(event_configuration)
    return event_configurations


def setup_module():
    global test_events
    test_events = setup_test_events()
    service_runner.run()


def teardown_module():
    service_runner.stop_running()


class TestStartup:
    def test_getting_identity(self):
        response = events_api_wrapper.get_index()
        assert isinstance(response['identity'], str)
        assert events_api_identity == response['identity']
        assert isinstance(response['version'], int)
        assert 2 == response['version']
        assert True is response['debug']


class TestEvents:
    def test_get_event_existence_of_existing_event(self):
        assert None is not None

    def test_get_event_existence_of_non_existent_event(self):
        assert None is not None

    def test_get_all_event_identifiers(self):
        assert None is not None

    def test_get_existing_event_info(self):
        assert None is not None

    def test_get_non_existent_event_info_returns_none(self):
        assert None is not None

    def test_register_new_event(self):
        assert None is not None

    def test_update_existing_event(self):
        assert None is not None

    def test_update_non_existent_event_throws_exception(self):
        assert None is not None

    def test_get_event_total(self):
        assert None is not None

    def test_get_event_total_of_non_existent_event_throws_exception(self):
        assert None is not None

    def test_update_event_total(self):
        assert None is not None

    def test_update_event_total_of_non_existent_event_throws_exception(self):
        assert None is not None
