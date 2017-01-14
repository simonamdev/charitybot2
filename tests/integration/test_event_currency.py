from charitybot2.botconfig.event_config import EventConfigurationFromFile
from charitybot2.events.currency import Currency
from charitybot2.events.event import Event
from tests.tests import TestFilePath, ResetDB

valid_config_path = TestFilePath().get_config_path('event', 'valid_config.json')
db_path = TestFilePath().get_repository_db_path()
db_script_path = TestFilePath().get_repository_script_path()

ResetDB(db_path=db_path, sql_path=db_script_path)
valid_event_config = EventConfigurationFromFile(file_path=valid_config_path)
valid_event = Event(event_configuration=valid_event_config, db_path=db_path)


class TestEventCurrency:
    def test_event_returns_expected_currency(self):
        assert isinstance(valid_event.get_currency(), Currency)
        assert 'GBP' == valid_event.get_currency().get_key()
        assert '£' == valid_event.get_currency().get_symbol()
