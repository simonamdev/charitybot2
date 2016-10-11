import os
import pytest
from charitybot2.events.events import Event
from charitybot2.events.event_config import EventConfiguration, InvalidEventConfigException


current_directory = os.path.dirname(os.path.abspath(__file__))
valid_config_path = os.path.join(current_directory, 'configs', 'valid_config' + '.' + EventConfiguration.config_format)
invalid_config_path = os.path.join(current_directory, 'configs', 'invalid_config' + '.' + EventConfiguration.config_format)


class TestEventConfigurationValidity:
    def test_invalid_config_throws_exception(self):
        with pytest.raises(InvalidEventConfigException):
            event = Event(config_path=invalid_config_path)

    def test_valid_config_loads_without_exception(self):
        event = Event(config_path=valid_config_path)
