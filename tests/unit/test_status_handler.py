from charitybot2.storage.db_handler import DBHandler
from charitybot2.storage.status_handler import StatusHandler
from tests.tests import TestFilePath, ResetDB

events_db_path = TestFilePath().get_db_path('events.db')
events_db_init_script_path = TestFilePath().get_db_path('events.sql')
donations_db_path = TestFilePath().get_db_path('donations.db')
donations_db_init_script_path = TestFilePath().get_db_path('donations.sql')

ResetDB(db_path=events_db_path, sql_path=events_db_init_script_path)
ResetDB(db_path=donations_db_path, sql_path=donations_db_init_script_path)
db_handler = DBHandler(events_db_path=events_db_path, donations_db_path=donations_db_path)


class TestStatusHandlerValidity:
    def test_initialise_with_valid_handler_starts_ok(self):
        status_handler = StatusHandler(db_handler=db_handler)
