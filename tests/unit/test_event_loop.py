import os
import pytest
from charitybot2.events.events import EventLoop
import charitybot2.storage.events_db as events_db
import charitybot2.events.event_config as event_config

current_directory = os.path.dirname(os.path.abspath(__file__))
events_db_path = os.path.join(current_directory, 'db', 'test_events.db')
valid_config_path = os.path.join(current_directory, 'configs', 'valid_config' + '.' + event_config.EventConfiguration.config_format)
invalid_config_path = os.path.join(current_directory, 'configs', 'invalid_config' + '.' + event_config.EventConfiguration.config_format)


class ValidEventLoop(EventLoop):
    def __init__(self):
        super().__init__(config_file_path=valid_config_path, db_path=events_db_path)


class InvalidEventLoop(EventLoop):
    def __init__(self):
        super().__init__(config_file_path=invalid_config_path, db_path=events_db_path)


class TestEventConfigurationValidity:
    def test_invalid_config_throws_exception(self):
        with pytest.raises(event_config.InvalidEventConfigException):
            e = InvalidEventLoop()

    def test_valid_config_loads_without_exception(self):
        e = ValidEventLoop()
