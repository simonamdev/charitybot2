import pytest
from charitybot2.creators.event_configuration_creator import InvalidEventConfigurationException, \
    EventConfigurationCreator
from charitybot2.creators.event_creator import EventRegister
from charitybot2.models.event import Event
from charitybot2.persistence.event_sqlite_repository import EventSQLiteRepository
from tests.mocks import WipeSQLiteDB
from tests.paths_for_tests import test_repository_db_path
from tests.unit.test_event_configuration_creator import get_updated_test_config_values

in_memory_event_repository = EventSQLiteRepository(debug=True)


def get_test_configuration(updated_values=None):
    test_event_configuration_creator = EventConfigurationCreator(
        configuration_values=get_updated_test_config_values(updated_values=updated_values))
    return test_event_configuration_creator.configuration


class TestEventRegister:
    def test_creating_unregistered_event(self):
        registration_test_configuration = get_test_configuration({'identifier': 'registration_test'})
        event_creator = EventRegister(event_configuration=registration_test_configuration,
                                      event_repository=in_memory_event_repository)
        assert event_creator.event_is_registered() is False
        new_event = event_creator.get_event()
        assert isinstance(new_event, Event)
        assert event_creator.event_is_registered() is True
        assert new_event.configuration.identifier == registration_test_configuration.identifier

    def test_updating_registered_event(self):
        sqlite_db_wipe = WipeSQLiteDB(db_path=test_repository_db_path)
        sqlite_db_wipe.wipe_db()
        test_event_repository = EventSQLiteRepository(db_path=test_repository_db_path)
        update_test_configuration = get_test_configuration({'identifier': 'update_event_test'})
        event_creator = EventRegister(
            event_configuration=update_test_configuration,
            event_repository=test_event_repository)
        assert event_creator.event_is_registered() is False
        test_event = event_creator.get_event()
        assert event_creator.event_is_registered() is True
        assert isinstance(test_event, Event)
        update_test_configuration = get_test_configuration(
            {'identifier': 'update_event_test', 'end_time': 999})
        event_creator = EventRegister(
            event_configuration=update_test_configuration,
            event_repository=test_event_repository)
        assert event_creator.event_is_registered() is True
        test_event = event_creator.get_event()
        assert event_creator.event_is_registered() is True
        assert test_event.configuration.end_time == update_test_configuration.end_time


class TestEventRegisterExceptions:
    @pytest.mark.parametrize('configuration', [
        None,
        123,
        'foobar',
        object
    ])
    def test_passing_incorrect_values_throws_exception(self, configuration):
        with pytest.raises(InvalidEventConfigurationException):
            event_creator = EventRegister(event_configuration=configuration, event_repository=None)
