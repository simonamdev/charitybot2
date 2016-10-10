import pytest
import os

from charitybot2.storage.events_db import EventsDB
from charitybot2.events.events import Event

current_directory = os.path.dirname(os.path.abspath(__file__))
valid_config_path = os.path.join(current_directory, 'configs', 'good_source_event_config.json')
test_db_path = os.path.join(current_directory, 'db', 'test_events.db')

e = Event(config_file_path=valid_config_path, db_path=test_db_path)
e.initialise_db_interface()


class TestEventStateChange:
    def test_register_new_event_successfully(self):
        e.register_event()
        edb = EventsDB(db_path=test_db_path)
        event_names = edb.get_all_event_names()
        event_metadata = edb.get_event_metadata(event_name='name')
        assert 'name' in event_names
        assert event_metadata['name'] == 'name'
        assert event_metadata['state'] == EventsDB.event_default_state

    def test_start_new_event_successfully(self):
        e.start_event()
        edb = EventsDB(db_path=test_db_path)
        event_metadata = edb.get_event_metadata(event_name='name')
        assert event_metadata['state'] == EventsDB.event_ongoing_state

    def test_complete_new_event_successfully(self):
        e.stop_event()
        edb = EventsDB(db_path=test_db_path)
        event_metadata = edb.get_event_metadata(event_name='name')
        assert event_metadata['state'] == EventsDB.event_completed_state
