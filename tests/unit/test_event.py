import os
import pytest
from charitybot2.events.events import Event
from charitybot2.events.event_config import EventConfiguration


current_directory = os.path.dirname(os.path.abspath(__file__))
valid_config_path = os.path.join(current_directory, 'configs', 'valid_config' + '.' + EventConfiguration.config_format)
invalid_config_path = os.path.join(current_directory, 'configs', 'invalid_config' + '.' + EventConfiguration.config_format)

