import pytest
import os
from charitybot2.events.events import Event

current_directory = os.path.dirname(os.path.abspath(__file__))
valid_config_path = os.path.join(current_directory, 'configs', 'good_source_event_config.json')

class TestEventRegistration:
    # Move to integration test
    def test_register_new_event_successfully(self):
        e = Event(config_file_path=valid_config_path, )
        e.initialise_db_interface()
        e.register_event()
