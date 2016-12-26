import pytest
from charitybot2.botconfig.event_config import EventConfigurationFromFile
from charitybot2.botconfig.json_config import InvalidConfigurationException
from charitybot2.events.event import Event
from charitybot2.storage.db_handler import DBHandler
from tests.tests import ResetDB, TestFilePath

valid_config_path = TestFilePath().get_config_path('event', 'valid_config.json')
invalid_config_path = TestFilePath().get_config_path('event', 'invalid_config.json')
donations_db_path = TestFilePath().get_db_path('donations.db')
donations_db_init_script_path = TestFilePath().get_db_path('donations.sql')

db_handler = DBHandler(donations_db_path=donations_db_path, debug=True)
valid_event_configuration = EventConfigurationFromFile(file_path=valid_config_path)
valid_event = Event(event_configuration=valid_event_configuration, db_handler=db_handler)


def setup_module():
    ResetDB(db_path=donations_db_path, sql_path=donations_db_init_script_path)


class TestEventRetrieve:
    def test_retrieve_event_name(self):
        assert valid_event.get_event_name() == 'name'

    def test_retrieve_channel_name(self):
        assert valid_event.get_channel_name() == 'channel'

    def test_retrieve_event_start_time(self):
        assert valid_event.get_start_time() == 0

    def test_retrieve_event_end_time(self):
        assert valid_event.get_end_time() == 9999999999999999

    def test_retrieve_event_target_amount(self):
        assert valid_event.get_target_amount() == 1000

    def test_retrieve_event_sources(self):
        source_url = valid_event.get_source_url()
        assert source_url == 'https://www.justgiving.com/fundraising/alasdair-clift'

    def test_retrieve_update_tick(self):
        assert valid_event.get_update_tick() == 5

    def test_retrieve_amount_raised(self):
        assert valid_event.get_amount_raised() == 0


class TestEventUpdate:
    def test_setting_amount_raised(self):
        valid_event.set_amount_raised(amount=100)
        assert valid_event.get_amount_raised() == 100

    def test_incrementing_amount_raised(self):
        valid_event.set_amount_raised(amount=200)
        valid_event.increment_amount_raised(amount_increase=50)
        assert valid_event.get_amount_raised() == 250
