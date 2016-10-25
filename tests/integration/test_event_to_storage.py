import os

import pytest

from charitybot2.storage.events_db import EventsDB, EventAlreadyRegisteredException
from charitybot2.events.event import Event
from charitybot2.charitybot2 import EventLoop
from tests.tests import ResetDB

current_directory = os.path.dirname(os.path.abspath(__file__))
valid_config_path = os.path.join(current_directory, 'configs', 'good_source_event_config.json')
test_db_path = os.path.join(current_directory, 'db', 'test_events.db')
events_db_init_script_path = os.path.join(current_directory, 'db', 'init_integration_test_events_db.sql')

ResetDB(db_path=test_db_path, sql_path=events_db_init_script_path)
event = Event(config_path=valid_config_path, db_path=test_db_path)
event_loop = EventLoop(event=event)


class TestEventStateChange:
    def test_register_new_event_successfully(self):
        event.register_event()
        edb = EventsDB(db_path=test_db_path)
        event_names = edb.get_all_event_names()
        event_metadata = edb.get_event_metadata(event_name='name')
        assert 'name' in event_names
        assert event_metadata['name'] == 'name'
        assert event_metadata['state'] == EventsDB.event_default_state

    def test_register_event_already_registered_throws_exception(self):
        with pytest.raises(EventAlreadyRegisteredException):
            event.register_event()

    def test_start_new_event_successfully(self):
        event.start_event()
        edb = EventsDB(db_path=test_db_path)
        event_metadata = edb.get_event_metadata(event_name='name')
        assert event_metadata['state'] == EventsDB.event_ongoing_state

    def test_complete_new_event_successfully(self):
        event.stop_event()
        edb = EventsDB(db_path=test_db_path)
        event_metadata = edb.get_event_metadata(event_name='name')
        assert event_metadata['state'] == EventsDB.event_completed_state
