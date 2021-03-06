import pytest
from charitybot2.creators.event_configuration_creator import InvalidEventConfigurationException
from charitybot2.creators.event_creator import EventRegister
from charitybot2.models.event import Event
from charitybot2.persistence.event_sqlite_repository import EventSQLiteRepository
from helpers.event_config import get_test_event_configuration


class TestEventRegister:
    test_event_repository = None

    def setup_method(self):
        self.test_event_repository = EventSQLiteRepository(debug=True)

    def teardown_method(self):
        self.test_event_repository.close_connection()

    def test_creating_unregistered_event(self):
        registration_test_configuration = get_test_event_configuration({'identifier': 'registration_test'})
        event_creator = EventRegister(
            event_configuration=registration_test_configuration,
            event_repository=self.test_event_repository)
        assert event_creator.event_is_registered() is False
        new_event = event_creator.get_event()
        assert isinstance(new_event, Event)
        assert event_creator.event_is_registered() is True
        assert new_event.configuration.identifier == registration_test_configuration.identifier

    def test_updating_registered_event(self):
        update_test_configuration = get_test_event_configuration({'identifier': 'update_event_test'})
        event_creator = EventRegister(
            event_configuration=update_test_configuration,
            event_repository=self.test_event_repository)
        assert event_creator.event_is_registered() is False
        test_event = event_creator.get_event()
        assert event_creator.event_is_registered() is True
        assert isinstance(test_event, Event)
        update_test_configuration = get_test_event_configuration(
            {'identifier': 'update_event_test', 'end_time': 999})
        event_creator = EventRegister(
            event_configuration=update_test_configuration,
            event_repository=self.test_event_repository)
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
