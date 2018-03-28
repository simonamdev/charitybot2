import pytest
from charitybot2.configurations.event_configuration import EventConfiguration
from charitybot2.creators.event_configuration_creator import EventConfigurationCreator
from charitybot2.persistence.event_sqlite_repository import EventSQLiteRepository, EventAlreadyRegisteredException, \
    EventNotRegisteredException
from helpers.event_config import get_updated_test_config_values

test_event_identifier = 'test_event'
starting_test_config = get_updated_test_config_values(updated_values={'identifier': test_event_identifier})
starting_test_configuration = EventConfigurationCreator(configuration_values=starting_test_config).configuration

non_existent_event_identifier = 'non_existent'
non_existent_config_values = get_updated_test_config_values(updated_values={'identifier': non_existent_event_identifier})
non_existent_event_configuration = EventConfigurationCreator(configuration_values=non_existent_config_values).configuration


class TestEventSQLiteRepository:
    test_event_repository = None

    def setup_method(self):
        self.test_event_repository = EventSQLiteRepository(debug=True)
        self.test_event_repository.register_event(event_configuration=starting_test_configuration)

    def teardown_method(self):
        self.test_event_repository.close_connection()

    def test_checking_if_non_existent_event_is_already_registered(self):
        assert self.test_event_repository.event_already_registered(identifier='registration_check') is False

    def test_for_existent_event_registration(self):
        assert self.test_event_repository.event_already_registered(identifier=test_event_identifier) is True

    def test_get_event_configuration(self):
        event_configuration = self.test_event_repository.get_event_configuration(identifier=test_event_identifier)
        assert isinstance(event_configuration, EventConfiguration)

    def test_registering_event(self):
        config_values = get_updated_test_config_values(updated_values={'identifier': 'new_event'})
        test_configuration = EventConfigurationCreator(configuration_values=config_values).configuration
        self.test_event_repository.register_event(event_configuration=test_configuration)
        assert self.test_event_repository.event_already_registered(identifier='new_event') is True
        retrieved_configuration = self.test_event_repository.get_event_configuration(test_configuration.identifier)
        assert test_configuration.identifier == retrieved_configuration.identifier
        assert test_configuration.source_url == retrieved_configuration.source_url

    def test_updating_event(self):
        config_values = get_updated_test_config_values(updated_values={'identifier': test_event_identifier, 'end_time': 999})
        new_test_configuration = EventConfigurationCreator(configuration_values=config_values).configuration
        self.test_event_repository.update_event(new_event_configuration=new_test_configuration)
        retrieved_configuration = self.test_event_repository.get_event_configuration(test_event_identifier)
        assert retrieved_configuration.end_time == 999

    def test_getting_event_starting_amount(self):
        assert 0 == self.test_event_repository.get_event_starting_amount(identifier=test_event_identifier)

    def test_updating_event_starting_amount(self):
        assert 0 == self.test_event_repository.get_event_starting_amount(identifier=test_event_identifier)
        self.test_event_repository.update_event_starting_amount(
            identifier=test_event_identifier,
            start_amount=500)
        assert 500 == self.test_event_repository.get_event_starting_amount(identifier=test_event_identifier)
        self.test_event_repository.update_event_starting_amount(
            identifier=test_event_identifier,
            start_amount=222.2)
        assert 222.2 == self.test_event_repository.get_event_starting_amount(identifier=test_event_identifier)

    def test_getting_event_current_amount(self):
        assert 0.0 == self.test_event_repository.get_event_current_amount(identifier=test_event_identifier)

    def test_updating_event_current_amount(self):
        assert 0 == self.test_event_repository.get_event_current_amount(identifier=test_event_identifier)
        self.test_event_repository.update_event_current_amount(
            identifier=test_event_identifier,
            current_amount=500)
        assert 500 == self.test_event_repository.get_event_current_amount(identifier=test_event_identifier)
        self.test_event_repository.update_event_current_amount(
            identifier=test_event_identifier,
            current_amount=222.2)
        assert 222.2 == self.test_event_repository.get_event_current_amount(identifier=test_event_identifier)

    def test_getting_list_of_events(self):
        # by default, test_event
        events = self.test_event_repository.get_events()
        assert 1 == len(events)
        assert 'test_event' == events[0].identifier
        # register an event
        config_values = get_updated_test_config_values(updated_values={'identifier': 'new_event'})
        test_configuration = EventConfigurationCreator(configuration_values=config_values).configuration
        self.test_event_repository.register_event(event_configuration=test_configuration)
        # check that the event is in the list now
        events = self.test_event_repository.get_events()
        assert 2 == len(events)
        assert 'new_event' == events[1].identifier
        # register another event
        config_values = get_updated_test_config_values(updated_values={'identifier': 'new_event_two'})
        test_configuration = EventConfigurationCreator(configuration_values=config_values).configuration
        self.test_event_repository.register_event(event_configuration=test_configuration)
        # check both events exist
        events = self.test_event_repository.get_events()
        assert 3 == len(events)
        # order should be newest first
        assert 'test_event' == events[0].identifier
        assert 'new_event' == events[1].identifier
        assert 'new_event_two' == events[2].identifier

    # An ongoing event is an event of which the current time is within the start and end time, +- some given buffer
    def test_getting_ongoing_events(self):
        # Register events
        number_of_test_events = 5
        number_of_test_events_including_original_test_event = number_of_test_events + 1
        for i in range(0, number_of_test_events):
            update_values = {
                'identifier': 'new_event_{}'.format(i),
                'start_time': 2,
                'end_time': 4
            }
            config_values = get_updated_test_config_values(updated_values=update_values)
            test_configuration = EventConfigurationCreator(configuration_values=config_values).configuration
            self.test_event_repository.register_event(event_configuration=test_configuration)
        # Test getting all ongoing events
        ongoing_events = self.test_event_repository.get_ongoing_events(current_time=3, buffer_in_minutes=0)
        assert number_of_test_events == len(ongoing_events)
        ongoing_events = self.test_event_repository.get_ongoing_events(current_time=3, buffer_in_minutes=1)
        assert number_of_test_events_including_original_test_event == len(ongoing_events)
        ongoing_events = self.test_event_repository.get_ongoing_events(current_time=999, buffer_in_minutes=0)
        assert 0 == len(ongoing_events)
        ongoing_events = self.test_event_repository.get_ongoing_events(current_time=65, buffer_in_minutes=1)
        assert 0 == len(ongoing_events)
        ongoing_events = self.test_event_repository.get_ongoing_events(current_time=64, buffer_in_minutes=1)
        assert number_of_test_events == len(ongoing_events)
        ongoing_events = self.test_event_repository.get_ongoing_events(current_time=64, buffer_in_minutes=2)
        assert number_of_test_events_including_original_test_event == len(ongoing_events)
        # Try to get the original test event only
        ongoing_events = self.test_event_repository.get_ongoing_events(current_time=0, buffer_in_minutes=0)
        assert 1 == len(ongoing_events)
        test_event = ongoing_events[0]
        assert 0 == test_event['start_time']
        assert 1 == test_event['end_time']
        assert test_event_identifier == test_event['identifier']

    def test_getting_ongoing_events_with_no_events_present_returns_empty_list(self):
        ongoing_events = self.test_event_repository.get_ongoing_events(current_time=3, buffer_in_minutes=0)
        assert 0 == len(ongoing_events)


class TestEventSQLiteRepositoryExceptions:
    test_event_repository = None

    def setup_method(self):
        self.test_event_repository = EventSQLiteRepository(debug=True)
        self.test_event_repository.register_event(event_configuration=starting_test_configuration)

    def teardown_method(self):
        self.test_event_repository.close_connection()

    def test_registering_already_registered_event_throws_exception(self):
        with pytest.raises(EventAlreadyRegisteredException):
            self.test_event_repository.register_event(event_configuration=starting_test_configuration)

    def test_updating_non_existent_event_throws_exception(self):
        with pytest.raises(EventNotRegisteredException):
            self.test_event_repository.update_event(new_event_configuration=non_existent_event_configuration)

    def test_getting_starting_amount_of_non_existent_event_throws_exception(self):
        with pytest.raises(EventNotRegisteredException):
            self.test_event_repository.get_event_starting_amount(identifier=non_existent_event_identifier)

    def test_updating_starting_amount_of_non_existent_event_throws_exception(self):
        with pytest.raises(EventNotRegisteredException):
            self.test_event_repository.update_event_starting_amount(
                identifier=non_existent_event_identifier,
                start_amount=5)

    def test_updating_current_amount_of_non_existent_event_throws_exception(self):
        with pytest.raises(EventNotRegisteredException):
            self.test_event_repository.update_event_current_amount(
                identifier=non_existent_event_identifier,
                current_amount=5)
