import pytest
from charitybot2.api.events_api import events_api, app, events_api_identity, port
from charitybot2.api_calls.events_api_wrapper import EventsApiWrapper
from charitybot2.models.event import NonExistentEventException
from charitybot2.paths import events_api_path, test_repository_db_path
from charitybot2.start_service import Service, ServiceRunner
from helpers.event_config import get_test_event_configuration
from helpers.setup_test_database import register_test_event, wipe_database

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

test_event_identifier_format = 'test_event_{}'
first_test_event_identifier = test_event_identifier_format.format(0)
non_existent_event_identifier = 'bla'


def setup_test_events(count=default_number_of_test_events):
    wipe_database(test_repository_db_path)
    test_internal_reference_string = test_event_identifier_format
    event_configurations = []
    for i in range(0, count):
        updated_values = {
            'identifier': test_internal_reference_string.format(i),
            'start_time': i,
            'end_time': i + 1
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
        test_event_exists = events_api_wrapper.get_event_exists(event_identifier=first_test_event_identifier)
        assert True is test_event_exists

    def test_get_event_existence_of_non_existent_event(self):
        non_existent_event_exists = events_api_wrapper.get_event_exists(event_identifier=non_existent_event_identifier)
        assert False is non_existent_event_exists

    def test_get_all_event_identifiers(self):
        event_identifiers = events_api_wrapper.get_event_identifiers()
        assert default_number_of_test_events == len(event_identifiers)
        for i in range(0, default_number_of_test_events):
            current_test_event_identifier = test_event_identifier_format.format(i)
            assert event_identifiers[i] == current_test_event_identifier

    def test_get_existing_event_info(self):
        event_info = events_api_wrapper.get_event_info(event_identifier=first_test_event_identifier)
        expected_start_time = 0
        expected_end_time = 1
        assert expected_start_time == event_info.start_time
        assert expected_end_time == event_info.end_time

    def test_get_non_existent_event_info_throws_exception(self):
        with pytest.raises(NonExistentEventException):
            non_existent_event_info = events_api_wrapper.get_event_info(event_identifier=non_existent_event_identifier)

    def test_register_new_event(self):
        # Generate a new event configuration
        new_test_event_identifier = 'creating_new_event_test'
        updated_values = {
            'identifier': new_test_event_identifier
        }
        test_event_configuration = get_test_event_configuration(updated_values=updated_values)
        # Check number of events before adding the new one
        event_identifiers = events_api_wrapper.get_event_identifiers()
        assert default_number_of_test_events == len(event_identifiers)
        # Register the new event
        successful = events_api_wrapper.register_event(event_configuration=test_event_configuration)
        assert True is successful
        # Check the number of events has increased
        event_identifiers = events_api_wrapper.get_event_identifiers()
        assert default_number_of_test_events + 1 == len(event_identifiers)
        assert event_identifiers[0] == new_test_event_identifier

    def test_update_existing_event(self):
        # Make sure that the event exists first
        event_exists = events_api_wrapper.get_event_exists(event_identifier=first_test_event_identifier)
        assert True is event_exists
        # Generate new details for an existing event
        new_start_time = 100
        new_end_time = 101
        new_target_amount = 333
        updated_values = {
            'identifier': first_test_event_identifier,
            'start_time': new_start_time,
            'end_time': new_end_time,
            'target_amount': new_target_amount
        }
        # generate a new event configuration
        new_test_event_configuration = get_test_event_configuration(updated_values=updated_values)
        events_api_wrapper.update_event(new_event_configuration=new_test_event_configuration)
        event_config = events_api_wrapper.get_event_info(event_identifier=first_test_event_identifier)
        assert first_test_event_identifier == event_config.identifier
        assert new_start_time == event_config.start_time
        assert new_end_time == event_config.end_time
        assert new_target_amount == event_config.target_amount

    def test_update_non_existent_event_throws_exception(self):
        updated_values = {
            'identifier': non_existent_event_identifier
        }
        new_non_existent_test_event_configuration = get_test_event_configuration(updated_values=updated_values)
        with pytest.raises(NonExistentEventException):
            events_api_wrapper.update_event(new_event_configuration=new_non_existent_test_event_configuration)

    def test_get_event_total(self):
        actual_test_event_amount = events_api_wrapper.get_event_total_raised(event_identifier=first_test_event_identifier)
        assert 0.0 == actual_test_event_amount

    def test_get_event_total_of_non_existent_event_throws_exception(self):
        with pytest.raises(NonExistentEventException):
            total = events_api_wrapper.get_event_total_raised(event_identifier=non_existent_event_identifier)

    def test_update_event_total(self):
        # Check it is zero
        actual_test_event_amount = events_api_wrapper.get_event_total_raised(
            event_identifier=first_test_event_identifier)
        assert 0.0 == actual_test_event_amount
        # Update it to an amount
        new_test_event_amount = 100.01
        events_api_wrapper.update_event_total(event_identifier=first_test_event_identifier, new_total=new_test_event_amount)
        # Retrieve the the new amount
        actual_test_event_amount = events_api_wrapper.get_event_total_raised(
            event_identifier=first_test_event_identifier)
        assert new_test_event_amount == actual_test_event_amount

    def test_update_event_total_passing_incorrectly_typed_value(self):
        # Update it to an amount
        new_test_event_amount = 'blablablalba'
        with pytest.raises(TypeError):
            events_api_wrapper.update_event_total(event_identifier=first_test_event_identifier, new_total=new_test_event_amount)

    def test_update_event_total_of_non_existent_event_throws_exception(self):
        with pytest.raises(NonExistentEventException):
             events_api_wrapper.update_event_total(event_identifier=non_existent_event_identifier, new_total=10.1)
