from charitybot2.configurations.event_configuration import EventConfiguration
from charitybot2.creators.event_configuration_creator import InvalidEventConfigurationException


class EventCreator:
    def __init__(self, event_configuration):
        self._event_configuration = event_configuration
        self.__validate_event_configuration()

    def __validate_event_configuration(self):
        if not isinstance(self._event_configuration, EventConfiguration):
            raise InvalidEventConfigurationException('Event creator can only accept Event Configurations')

    def get_event(self):
        pass

    def event_is_registered(self, event_identifier):
        pass
