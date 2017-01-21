import pytest

from charitybot2.botconfig.event_config import EventConfigurationFromFile, EventConfigurationCreator, EventConfiguration
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
        assert 'USD' == valid_event.get_configuration().get_currency().get_key()
        valid_event.update_event(event_configuration=valid_event_configuration)
        assert 'GBP' == valid_event.get_configuration().get_currency().get_key()


class TestEventRetrieve:
    @pytest.mark.parametrize('expected,actual', [
        (True, isinstance(valid_event.get_configuration(), EventConfiguration)),
        (0, valid_event.get_starting_amount()),
        (0, valid_event.get_amount_raised())
    ])
    def test_retrieval(self, expected, actual):
        assert expected == actual


class TestEventUpdate:
    def test_setting_amount_raised(self):
        valid_event.set_amount_raised(amount=100)
        assert valid_event.get_amount_raised() == 100

    def test_incrementing_amount_raised(self):
        valid_event.set_amount_raised(amount=200)
        valid_event.increment_amount_raised(amount_increase=50)
        assert valid_event.get_amount_raised() == 250

