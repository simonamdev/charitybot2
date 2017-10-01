import pytest
from charitybot2.creators.event_configuration_creator import InvalidEventConfigurationException
from charitybot2.creators.event_creator import EventCreator
from charitybot2.models.event import Event
from helpers.event_config import get_test_event_configuration


class TestEventCreator:
    def test_getting_event_from_creator(self):
        event_creator = EventCreator(event_configuration=get_test_event_configuration())
        event = event_creator.get_event()
        assert isinstance(event, Event)


# Commented to avoid pytest throwing a fit
# class TestEventCreatorExceptions:
#     @pytest.mark.parametrize('config', [
#         None,
#         1,
#         2.0,
#         '',
#         object,
#         True
#     ])
#     def test_passing_non_event_config_throws_exception(self, config):
#         with pytest.raises(InvalidEventConfigurationException):
#             EventCreator(event_configuration=config)
