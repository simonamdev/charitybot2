import pytest

from charitybot2.charitybot2 import EventLoop
from charitybot2.events.event import Event
from charitybot2.storage.db_handler import DBHandler
from charitybot2.storage.events_db import EventsDB, EventAlreadyRegisteredException
from tests.tests import ResetDB, TestFilePath

valid_config_path = TestFilePath().get_config_path('good_source_event_config.json')
events_db_path = TestFilePath().get_db_path('events.db')
events_db_init_script_path = TestFilePath().get_db_path('events.sql')
donations_db_path = TestFilePath().get_db_path('donations.db')
donations_db_init_script_path = TestFilePath().get_db_path('donations.sql')

ResetDB(db_path=events_db_path, sql_path=events_db_init_script_path)
ResetDB(db_path=donations_db_path, sql_path=donations_db_init_script_path)
db_handler = DBHandler(events_db_path=events_db_path, donations_db_path=donations_db_path)
event = Event(config_path=valid_config_path, db_handler=db_handler)
event_loop = EventLoop(event=event)


class TestEventStateChange:
    def test_register_new_event_successfully(self):
        event.register_event()
        edb = EventsDB(db_path=events_db_path)
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
        edb = EventsDB(db_path=events_db_path)
        event_metadata = edb.get_event_metadata(event_name='name')
        assert event_metadata['state'] == EventsDB.event_ongoing_state

    def test_complete_new_event_successfully(self):
        event.stop_event()
        edb = EventsDB(db_path=events_db_path)
        event_metadata = edb.get_event_metadata(event_name='name')
        assert event_metadata['state'] == EventsDB.event_completed_state
