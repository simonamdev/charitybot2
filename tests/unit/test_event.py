import os
from time import sleep

import pytest
from charitybot2.events.events import Event
from charitybot2.events.event_config import EventConfiguration, InvalidEventConfigException
from tests.tests import ResetDB

current_directory = os.path.dirname(os.path.abspath(__file__))
valid_config_path = os.path.join(current_directory, 'configs', 'valid_config' + '.' + EventConfiguration.config_format)
invalid_config_path = os.path.join(current_directory, 'configs', 'invalid_config' + '.' + EventConfiguration.config_format)
events_db_path = os.path.join(current_directory, 'db', 'test_events.db')
events_db_init_script_path = os.path.join(current_directory, 'db', 'init_test_events.sql')

ResetDB(db_path=events_db_path, sql_path=events_db_init_script_path)
valid_event = Event(config_path=valid_config_path, db_path=events_db_path)


class TestEventConfigurationValidity:
    def test_invalid_config_throws_exception(self):
        with pytest.raises(InvalidEventConfigException):
            event = Event(config_path=invalid_config_path, db_path=events_db_path)

    def test_valid_config_loads_without_exception(self):
        event = Event(config_path=valid_config_path, db_path=events_db_path)


class TestEventRetrieve:
    def test_retrieve_event_name(self):
        assert valid_event.get_event_name() == 'name'

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
