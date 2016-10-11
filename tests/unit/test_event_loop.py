import os
import pytest
from charitybot2.events.events import EventLoop, Event
import charitybot2.storage.events_db as events_db
import charitybot2.events.event_config as event_config

current_directory = os.path.dirname(os.path.abspath(__file__))
events_db_path = os.path.join(current_directory, 'db', 'test_events.db')
valid_config_path = os.path.join(current_directory, 'configs', 'valid_config' + '.' + event_config.EventConfiguration.config_format)
invalid_config_path = os.path.join(current_directory, 'configs', 'invalid_config' + '.' + event_config.EventConfiguration.config_format)


class ValidTestEvent(Event):
    def __init__(self):
        super().__init__(config_path=valid_config_path)


class InvalidTestEvent(Event):
    def __init__(self):
        super().__init__(config_path=invalid_config_path)
