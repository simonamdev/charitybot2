from charitybot2.storage.db_handler import DBHandler
from charitybot2.storage.events_db import EventMetadata
from charitybot2.storage.status_handler import StatusHandler
from tests.tests import TestFilePath, ResetDB

events_db_path = TestFilePath().get_db_path('events.db')
events_db_init_script_path = TestFilePath().get_db_path('events.sql')
donations_db_path = TestFilePath().get_db_path('donations.db')
donations_db_init_script_path = TestFilePath().get_db_path('donations.sql')

ResetDB(db_path=events_db_path, sql_path=events_db_init_script_path)
ResetDB(db_path=donations_db_path, sql_path=donations_db_init_script_path)
db_handler = DBHandler(events_db_path=events_db_path, donations_db_path=donations_db_path, debug=True)
status_handler = StatusHandler(db_handler=db_handler)


class TestStatusHandlerRetrieve:
    def test_retrieving_registered_event_metadata(self):
        running_events = status_handler.get_events(state=EventMetadata.registered_state)
        for metadata in running_events:
            assert EventMetadata.registered_state == metadata.get_state()

    def test_retrieving_ongoing_event_metadata(self):
        running_events = status_handler.get_events(state=EventMetadata.ongoing_state)
        for metadata in running_events:
            assert EventMetadata.ongoing_state == metadata.get_state()
