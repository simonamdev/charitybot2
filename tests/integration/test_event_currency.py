from charitybot2.botconfig.event_config import EventConfigurationFromFile
from charitybot2.events.currency import Currency
from charitybot2.events.event import Event
from tests.mocks import ResetDB
from tests.paths_for_tests import valid_config_path, repository_db_path, repository_db_script_path

ResetDB(db_path=repository_db_path, sql_path=repository_db_script_path)
valid_event_config = EventConfigurationFromFile(file_path=valid_config_path)
valid_event = Event(event_configuration=valid_event_config, db_path=repository_db_path)


class TestEventCurrency:
    def test_event_returns_expected_currency(self):
        assert isinstance(valid_event.get_currency(), Currency)
        assert 'GBP' == valid_event.get_currency().get_key()
        assert '£' == valid_event.get_currency().get_symbol()
