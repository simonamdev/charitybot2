from charitybot2.botconfig.event_config import EventConfigurationFromFile
from charitybot2.events.event import Event
from tests.test_helpers import ResetDB, TestFilePath

valid_config_path = TestFilePath().get_config_path('event', 'valid_config.json')
db_path = TestFilePath().get_repository_db_path()
db_script_path = TestFilePath().get_repository_script_path()

valid_event_configuration = EventConfigurationFromFile(file_path=valid_config_path)
valid_event = Event(event_configuration=valid_event_configuration, db_path=db_path)


def setup_module():
    ResetDB(db_path=db_path, sql_path=db_script_path)


class TestEventRetrieve:
    def test_valid_event_is_not_already_registered(self):
        assert valid_event.event_already_registered() is False

    def test_registering_event(self):
        valid_event.register_or_update_event()

    def test_retrieve_internal_name(self):
        assert valid_event.get_internal_name() == 'valid_configured_event'

    def test_retrieve_external_name(self):
        assert valid_event.get_external_name() == 'Valid Configured Event'

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
