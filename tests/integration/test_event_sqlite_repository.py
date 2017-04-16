import copy

import pytest
from charitybot2.configurations.event_configuration import EventConfiguration
from charitybot2.creators.event_configuration_creator import EventConfigurationCreator
from charitybot2.persistence.event_sqlite_repository import EventSQLiteRepository, EventAlreadyRegisteredException, \
    EventNotRegisteredException
from tests.unit.test_event_configuration import test_event_configuration_values


def get_updated_config_values(updates=None):
    config_values = copy.deepcopy(test_event_configuration_values)
    if updates is not None:
        config_values.update(updates)
    return config_values


test_event_identifier = 'test_event'
starting_test_config = get_updated_config_values(updates={'identifier': test_event_identifier})
starting_test_configuration = EventConfigurationCreator(configuration_values=starting_test_config).configuration

non_existent_event_identifier = 'non_existent'
non_existent_config_values = get_updated_config_values(updates={'identifier': non_existent_event_identifier})
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
        assert self.test_event_repository.event_already_registered(identifier='test_event') is True

    def test_get_event_configuration(self):
        event_configuration = self.test_event_repository.get_event_configuration(identifier='test_event')
        assert isinstance(event_configuration, EventConfiguration)

    def test_registering_event(self):
        config_values = get_updated_config_values(updates={'identifier': 'new_event'})
        test_configuration = EventConfigurationCreator(configuration_values=config_values).configuration
        self.test_event_repository.register_event(event_configuration=test_configuration)
        assert self.test_event_repository.event_already_registered(identifier='new_event') is True
        retrieved_configuration = self.test_event_repository.get_event_configuration(test_configuration.identifier)
        assert test_configuration.identifier == retrieved_configuration.identifier
        assert test_configuration.source_url == retrieved_configuration.source_url

    def test_updating_event(self):
        config_values = get_updated_config_values(updates={'identifier': test_event_identifier, 'end_time': 999})
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
