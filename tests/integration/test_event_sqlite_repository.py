import copy

import pytest
from charitybot2.configurations.event_configuration import EventConfiguration
from charitybot2.creators.event_configuration_creator import EventConfigurationCreator
from charitybot2.persistence.event_sqlite_repository import EventSQLiteRepository, EventAlreadyRegisteredException, \
    EventNotRegisteredException
from charitybot2.persistence.sqlite_repository import InvalidRepositoryException
from tests.paths_for_tests import test_repository_db_path
from tests.unit.test_event_configuration import test_event_configuration_values


def get_updated_config_values(updates=None):
    config_values = copy.deepcopy(test_event_configuration_values)
    if updates is not None:
        config_values.update(updates)
    return config_values


starting_test_config = get_updated_config_values(updates={'identifier': 'test_event_1'})
starting_test_configuration = EventConfigurationCreator(configuration_values=starting_test_config).configuration

test_event_repository = EventSQLiteRepository(debug=True)
test_event_repository.register_event(event_configuration=starting_test_configuration)


class TestEventSQLiteRepositoryInstantiation:
    def test_default_debug_is_false(self):
        event_repository = EventSQLiteRepository(db_path=test_repository_db_path)
        assert event_repository.debug is False

    @pytest.mark.parametrize('debug,path', [
        (True, ':memory:'),
        (False, test_repository_db_path)
    ])
    def test_repository_paths(self, debug, path):
        event_repository = EventSQLiteRepository(db_path=test_repository_db_path, debug=debug)
        assert event_repository.db_path == path


class TestEventSQLiteRepository:
    def test_checking_if_event_is_already_registered(self):
        assert test_event_repository.event_already_registered(identifier='registration_check') is False

    def test_get_event_configuration(self):
        event_configuration = test_event_repository.get_event_configuration(identifier='test_event_1')
        assert isinstance(event_configuration, EventConfiguration)

    def test_registering_event(self):
        config_values = get_updated_config_values(updates={'identifier': 'event_registration_test'})
        test_configuration = EventConfigurationCreator(configuration_values=config_values).configuration
        test_event_repository.register_event(event_configuration=test_configuration)
        assert test_event_repository.event_already_registered(identifier='event_registration_test') is True
        retrieved_configuration = test_event_repository.get_event_configuration(test_configuration.identifier)
        assert test_configuration.identifier == retrieved_configuration.identifier
        assert test_configuration.source_url == retrieved_configuration.source_url

    def test_updating_event(self):
        config_values = get_updated_config_values(updates={'identifier': 'event_update_test'})
        test_configuration = EventConfigurationCreator(configuration_values=config_values).configuration
        assert test_configuration.end_time == 1
        test_event_repository.register_event(event_configuration=test_configuration)
        config_values = get_updated_config_values(updates={'identifier': 'event_update_test', 'end_time': 999})
        new_test_configuration = EventConfigurationCreator(configuration_values=config_values).configuration
        test_event_repository.update_event(new_event_configuration=new_test_configuration)
        retrieved_configuration = test_event_repository.get_event_configuration(test_configuration.identifier)
        assert retrieved_configuration.end_time == 999

    def test_getting_event_starting_amount(self):
        config_values = get_updated_config_values(updates={'identifier': 'start_amount_get_test'})
        test_configuration = EventConfigurationCreator(configuration_values=config_values).configuration
        test_event_repository.register_event(event_configuration=test_configuration)
        assert 0 == test_event_repository.get_event_starting_amount(identifier=test_configuration.identifier)

    def test_updating_event_starting_amount(self):
        config_values = get_updated_config_values(updates={'identifier': 'start_amount_update_test'})
        test_configuration = EventConfigurationCreator(configuration_values=config_values).configuration
        test_event_repository.register_event(event_configuration=test_configuration)
        assert 0 == test_event_repository.get_event_starting_amount(identifier=test_configuration.identifier)
        test_event_repository.update_event_starting_amount(identifier=test_configuration.identifier, start_amount=500)
        assert 500 == test_event_repository.get_event_starting_amount(identifier=test_configuration.identifier)
        test_event_repository.update_event_starting_amount(identifier=test_configuration.identifier, start_amount=222.2)
        assert 222.2 == test_event_repository.get_event_starting_amount(identifier=test_configuration.identifier)


class TestEventSQLiteRepositoryExceptions:
    def test_passing_no_db_path_in_production_mode_throws_exception(self):
        with pytest.raises(InvalidRepositoryException):
            EventSQLiteRepository(db_path='', debug=False)

    def test_registering_already_registered_event_throws_exception(self):
        config_values = get_updated_config_values(updates={'identifier': 'already_registered'})
        test_configuration = EventConfigurationCreator(configuration_values=config_values).configuration
        test_event_repository.register_event(event_configuration=test_configuration)
        with pytest.raises(EventAlreadyRegisteredException):
            test_event_repository.register_event(event_configuration=test_configuration)

    def test_updating_non_existent_event_throws_exception(self):
        config_values = get_updated_config_values(updates={'identifier': 'not_registered'})
        test_configuration = EventConfigurationCreator(configuration_values=config_values).configuration
        with pytest.raises(EventNotRegisteredException):
            test_event_repository.update_event(new_event_configuration=test_configuration)

    def test_getting_starting_amount_of_non_existent_event_throws_exception(self):
        config_values = get_updated_config_values(updates={'identifier': 'not_registered'})
        test_configuration = EventConfigurationCreator(configuration_values=config_values).configuration
        with pytest.raises(EventNotRegisteredException):
            test_event_repository.get_event_starting_amount(identifier=test_configuration.identifier)

    def test_updating_starting_amount_of_non_existent_event_throws_exception(self):
        config_values = get_updated_config_values(updates={'identifier': 'not_registered'})
        test_configuration = EventConfigurationCreator(configuration_values=config_values).configuration
        with pytest.raises(EventNotRegisteredException):
            test_event_repository.update_event_starting_amount(identifier=test_configuration.identifier, start_amount=5)

