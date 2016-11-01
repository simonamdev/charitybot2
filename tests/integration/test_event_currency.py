from charitybot2.events.currency import Currency
from charitybot2.events.event import Event
from charitybot2.storage.db_handler import DBHandler
from tests.tests import TestFilePath, ResetDB

valid_config_path = TestFilePath().get_config_path('event', 'valid_config.json')
donations_db_path = TestFilePath().get_db_path('donations.db')
donations_db_init_script_path = TestFilePath().get_db_path('donations.sql')

ResetDB(db_path=donations_db_path, sql_path=donations_db_init_script_path)
db_handler = DBHandler(donations_db_path=donations_db_path)
valid_event = Event(config_path=valid_config_path, db_handler=db_handler)


class TestEventCurrency:
    def test_event_returns_expected_currency(self):
        assert isinstance(valid_event.get_currency(), Currency)
        assert '£' == valid_event.get_currency().get_symbol()
