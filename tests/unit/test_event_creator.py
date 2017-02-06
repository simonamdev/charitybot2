import pytest
from charitybot2.creators.event_configuration_creator import InvalidEventConfigurationException, \
    EventConfigurationCreator
from charitybot2.creators.event_creator import EventCreator
from charitybot2.models.event import Event
from tests.unit.test_event_configuration_creator import get_updated_test_config_values

test_event_configuration = get_updated_test_config_values()


def get_test_configuration(updated_values=None):
    test_event_configuration_creator = EventConfigurationCreator(
        configuration_values=get_updated_test_config_values(updated_values=updated_values))
    return test_event_configuration_creator.configuration


class TestEventCreation:
    def test_creating_unregistered_event(self):
        registration_test_configuration = get_test_configuration({'identifier': 'registration_test'})
        event_creator = EventCreator(event_configuration=test_event_configuration)
        assert event_creator.event_is_registered(event_identifier=registration_test_configuration.identifier) is False
        new_event = event_creator.get_event()
        assert isinstance(new_event, Event)
        assert new_event.configuration.identifier == registration_test_configuration.identifier
        assert event_creator.event_is_registered(event_identifier=registration_test_configuration.identifier) is True

    def test_updating_registered_event(self):
        update_test_configuration = get_test_configuration({'identifier': 'update_event_test'})
        event_creator = EventCreator(event_configuration=update_test_configuration)
        test_event = event_creator.get_event()
        assert isinstance(test_event, Event)
        assert event_creator.event_is_registered(test_event) is True
        update_test_configuration = get_test_configuration({'end_time': 999})
        event_creator = EventCreator(event_configuration=update_test_configuration)
        test_event = event_creator.get_event()
        assert event_creator.event_is_registered(test_event) is True
        assert test_event.configuration.end_time == update_test_configuration.end_time


class TestEventCreatorExceptions:
    @pytest.mark.parametrize('configuration', [
        None,
        123,
        'foobar',
        object
    ])
    def test_passing_incorrect_values_throws_exception(self, configuration):
        with pytest.raises(InvalidEventConfigurationException):
            event_creator = EventCreator(event_configuration=configuration)
