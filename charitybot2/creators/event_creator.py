import time
from charitybot2.configurations.event_configuration import EventConfiguration
from charitybot2.creators.event_configuration_creator import InvalidEventConfigurationException
from charitybot2.models.event import Event
from charitybot2.persistence.event_repository import EventRepository
from charitybot2.persistence.logger import Logger


class EventCreator:
    def __init__(self, event_configuration, debug=False):
        self._configuration = event_configuration
        self._debug = debug
        self.__validate_event_configuration()
        self._logger = Logger(source='EventCreator', event=self._configuration.identifier)

    @property
    def debug(self):
        return self._debug

    def get_event(self):
        if self.event_is_registered():
            self._update_event()
        else:
            self._register_event()
        return Event(configuration=self._configuration)

    def __validate_event_configuration(self):
        if not isinstance(self._configuration, EventConfiguration):
            raise InvalidEventConfigurationException('Event creator can only accept Event Configurations')

    def _register_event(self):
        pass

    def _update_event(self):
        pass

    def event_is_registered(self):
        event_repository = EventRepository(debug=self.debug)
        registered = event_repository.event_already_registered(identifier=self._configuration.identifier)
        event_repository.close_connection()
        if registered:
            self._logger.log_info(timestamp=int(time.time()), message='Event is already registered')
        else:
            self._logger.log_info(timestamp=int(time.time()), message='Event is not registered yet')
        return registered
