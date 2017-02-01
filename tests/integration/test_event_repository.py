import copy

import pytest
from charitybot2.configurations.event_configuration import EventConfiguration
from charitybot2.creators.event_configuration_creator import EventConfigurationCreator
from charitybot2.paths import production_repository_db_path
from charitybot2.persistence.event_repository import EventRepository, EventAlreadyRegisteredException, \
    EventNotRegisteredException
from tests.paths_for_tests import test_repository_db_path, valid_event_config_path
from tests.unit.test_event_configuration import test_event_configuration_values

test_event_repository = EventRepository(debug=True)


class TestEventRepositoryInstantiation:
    def test_default_debug_is_false(self):
        event_repository = EventRepository()
        assert event_repository.debug is False

    @pytest.mark.parametrize('debug,path', [
        (True, test_repository_db_path),
        (False, production_repository_db_path)
    ])
    def test_repository_paths(self, debug, path):
        event_repository = EventRepository(debug=debug)
        assert event_repository.db_path == path


class TestEventRepository:
    def test_get_event_configuration(self):
        event_configuration = test_event_repository.get_event_configuration(identifier='test_event_1')
        assert isinstance(event_configuration, EventConfiguration)

    def test_registering_event(self):
        config_values = copy.deepcopy(test_event_configuration_values)
        config_values['identifier'] = 'event_registration_test'
        test_configuration = EventConfigurationCreator(configuration_values=config_values).configuration
        test_event_repository.register_event(event_configuration=test_configuration)
        retrieved_configuration = test_event_repository.get_event_configuration(test_configuration.identifier)
        assert test_configuration.identifier == retrieved_configuration.identifier
        assert test_configuration.source_url == retrieved_configuration.source_url

    def test_updating_event(self):
        config_values = copy.deepcopy(test_event_configuration_values)
        config_values['identifier'] = 'event_update_test'
        test_configuration = EventConfigurationCreator(configuration_values=config_values).configuration
        assert test_configuration.end_time == 1
        test_event_repository.register_event(event_configuration=test_configuration)
        config_values['end_time'] = 999
        new_test_configuration = EventConfigurationCreator(configuration_values=config_values).configuration
        test_event_repository.update_event(new_event_configuration=new_test_configuration)
        retrieved_configuration = test_event_repository.get_event_configuration(test_configuration.identifier)
        assert retrieved_configuration.end_time == 999


class TestEventRepositoryExceptions:
    def test_registering_already_registered_event_throws_exception(self):
        config_values = copy.deepcopy(test_event_configuration_values)
        config_values['identifier'] = 'already_registered'
        test_configuration = EventConfigurationCreator(configuration_values=config_values).configuration
        test_event_repository.register_event(event_configuration=test_configuration)
        with pytest.raises(EventAlreadyRegisteredException):
            test_event_repository.register_event(event_configuration=test_configuration)

    def test_updating_non_existent_event_throws_exception(self):
        config_values = copy.deepcopy(test_event_configuration_values)
        config_values['identifier'] = 'not_registered'
        test_configuration = EventConfigurationCreator(configuration_values=config_values).configuration
        with pytest.raises(EventNotRegisteredException):
            test_event_repository.update_event(new_event_configuration=test_configuration)
