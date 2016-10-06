import os
import pytest
from charitybot2.events.events import Event
import charitybot2.storage.events_db as events_db
import charitybot2.events.event_config as event_config

current_directory = os.path.dirname(os.path.abspath(__file__))
valid_config_path = os.path.join(current_directory, 'configs', 'valid_config' + '.' + event_config.EventConfiguration.config_format)
invalid_config_path = os.path.join(current_directory, 'configs', 'invalid_config' + '.' + event_config.EventConfiguration.config_format)


class TestEventConfigurationValidity:
    def test_invalid_config_throws_exception(self):
        with pytest.raises(event_config.InvalidEventConfigException):
            e = Event(config_file_path=invalid_config_path)
