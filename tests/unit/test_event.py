from charitybot2.botconfig.event_config import EventConfigurationFromFile, EventConfigurationCreator
from charitybot2.events.event import Event
from charitybot2.storage.repository import Repository
from tests.mocks import ResetDB
from tests.paths_for_tests import valid_config_path, repository_db_script_path, repository_db_path

repository = Repository(db_path=repository_db_path)

valid_event_configuration = EventConfigurationFromFile(file_path=valid_config_path).get_event_configuration()
valid_event = Event(event_configuration=valid_event_configuration, db_path=repository_db_path)


def setup_module():
    ResetDB(db_path=repository_db_path, sql_path=repository_db_script_path)


class TestEventRegistration:
    def test_valid_event_is_not_already_registered(self):
        assert valid_event.event_already_registered() is False

    def test_registering_event(self):
        assert False is repository.event_exists(event_name='valid_configured_event')
        assert False is valid_event.event_already_registered()
        valid_event.register_event()
        assert True is repository.event_exists(event_name='valid_configured_event')
        assert True is valid_event.event_already_registered()

    def test_updating_event_configuration(self):
        config_data = EventConfigurationFromFile(file_path=valid_config_path).get_config_data()
        config_data['currency_key'] = 'USD'
        new_currency_config = EventConfigurationCreator(config_values=config_data).get_event_configuration()
        valid_event.update_event(event_configuration=new_currency_config)
        assert 'USD' == valid_event.get_currency().get_key()
        print(valid_event_configuration.get_value('currency_key'))
        valid_event.update_event(event_configuration=valid_event_configuration)
        assert 'GBP' == valid_event.get_currency().get_key()


class TestEventRetrieve:
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

    def test_retrieve_starting_amount(self):
        assert valid_event.get_starting_amount() == 0


class TestEventUpdate:
    def test_setting_amount_raised(self):
        valid_event.set_amount_raised(amount=100)
        assert valid_event.get_amount_raised() == 100

    def test_incrementing_amount_raised(self):
        valid_event.set_amount_raised(amount=200)
        valid_event.increment_amount_raised(amount_increase=50)
        assert valid_event.get_amount_raised() == 250

