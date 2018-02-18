import pytest
from charitybot2.creators.event_configuration_creator import EventConfigurationCreator

from charitybot2.models.donation import Donation
from charitybot2.persistence.event_sqlite_repository import EventNotRegisteredException, EventAlreadyRegisteredException, \
    EventInvalidValueException
from charitybot2.services.events_service import EventsService
from helpers.event_config import get_updated_test_config_values

test_range_min = 1
test_range_max = 6
test_range = range(test_range_min, test_range_max)
test_event_identifier = 'event_service-test_event'
non_existent_event = 'foofoofoo'


def dictionaries_are_the_same(dict_a, dict_b):
    return len(set(dict_a.items() ^ dict_b.items())) == 0


def get_test_event_config(updated_values=None):
    values = {'identifier': test_event_identifier}
    if updated_values:
       values.update(updated_values)
    test_config_values = get_updated_test_config_values(updated_values=values)
    return EventConfigurationCreator(configuration_values=test_config_values).configuration


def register_test_event(service):
    service._event_repository.register_event(get_test_event_config())


class TestEventsService:
    events_service = None

    def setup_method(self):
        self.events_service = EventsService(repository_path='memory')
        self.events_service.open_connections()
        register_test_event(self.events_service)

    def teardown_method(self):
        self.events_service.close_connections()

    def test_get_all_event_identifiers(self):
        event_identifiers = self.events_service.get_all_event_identifiers()
        assert 1 == len(event_identifiers)
        assert test_event_identifier == event_identifiers[0]

    def test_existing_event_is_registered(self):
        registered = self.events_service.event_is_registered(event_identifier=test_event_identifier)
        assert True is registered

    def test_non_existent_event_is_not_registered(self):
        registered = self.events_service.event_is_registered(event_identifier=non_existent_event)
        assert False is registered

    def test_retrieving_existing_event_configuration(self):
        expected_values = get_updated_test_config_values(updated_values={'identifier': test_event_identifier})
        actual_configuration = self.events_service.get_event_configuration(event_identifier=test_event_identifier)
        actual_values = actual_configuration.configuration_values
        assert True is dictionaries_are_the_same(expected_values, actual_values)

    def test_retrieving_non_existent_event_configuration_throws_exception(self):
        with pytest.raises(EventNotRegisteredException):
            self.events_service.get_event_configuration(event_identifier=non_existent_event)

    def test_register_event(self):
        assert 1 == len(self.events_service.get_all_event_identifiers())
        test_identifier = 'event_registration_test'
        event_config = get_test_event_config(updated_values={'identifier': test_identifier})
        self.events_service.register_event(event_configuration=event_config)
        assert 2 == len(self.events_service.get_all_event_identifiers())
        expected_event_config_values = get_updated_test_config_values(updated_values={'identifier': test_identifier})
        actual_event_config = self.events_service.get_event_configuration(event_identifier=test_identifier)
        actual_event_config_values = actual_event_config.configuration_values
        assert True is dictionaries_are_the_same(expected_event_config_values, actual_event_config_values)

    def test_registering_already_registered_event_throws_exception(self):
        event_config = get_test_event_config()
        with pytest.raises(EventAlreadyRegisteredException):
            self.events_service.register_event(event_configuration=event_config)

    def test_updating_existing_event(self):
        # Register the event
        test_identifier = 'event_update_test'
        event_config = get_test_event_config(updated_values={'identifier': test_identifier})
        self.events_service.register_event(event_configuration=event_config)
        # Update the event
        test_target_amount = 3333333
        updated_event_config = get_test_event_config(
            updated_values={'target_amount': test_target_amount, 'identifier': test_identifier})
        self.events_service.update_event(event_configuration=updated_event_config)
        # retrieve the config
        actual_config = self.events_service.get_event_configuration(event_identifier=test_identifier)
        expected_config_values = updated_event_config.configuration_values
        actual_config_values = actual_config.configuration_values
        assert True is dictionaries_are_the_same(expected_config_values, actual_config_values)

    def test_updating_non_existent_event_throws_exception(self):
        event_config = get_test_event_config(updated_values={'identifier': non_existent_event})
        with pytest.raises(EventNotRegisteredException):
            self.events_service.update_event(event_configuration=event_config)

    def test_getting_event_total(self):
        expected_total = 0.0
        actual_total = self.events_service.get_event_total(event_identifier=test_event_identifier)
        assert expected_total == actual_total

    def test_getting_event_total_of_non_existent_event_throws_exception(self):
        with pytest.raises(EventNotRegisteredException):
            self.events_service.get_event_total(event_identifier=non_existent_event)

    def test_setting_event_total(self):
        expected_total = 5.5
        self.events_service.set_event_total(event_identifier=test_event_identifier, total=expected_total)
        actual_total = self.events_service.get_event_total(event_identifier=test_event_identifier)
        assert expected_total == actual_total

    def test_setting_non_existent_event_total_throws_exception(self):
        with pytest.raises(EventNotRegisteredException):
            self.events_service.set_event_total(event_identifier=non_existent_event, total=5.5)
