import os
import pytest
from charitybot2.events.events import Event
from charitybot2.events.event_config import EventConfiguration, InvalidEventConfigException


current_directory = os.path.dirname(os.path.abspath(__file__))
valid_config_path = os.path.join(current_directory, 'configs', 'valid_config' + '.' + EventConfiguration.config_format)
invalid_config_path = os.path.join(current_directory, 'configs', 'invalid_config' + '.' + EventConfiguration.config_format)

valid_event = Event(config_path=valid_config_path)


class TestEventConfigurationValidity:
    def test_invalid_config_throws_exception(self):
        with pytest.raises(InvalidEventConfigException):
            event = Event(config_path=invalid_config_path)

    def test_valid_config_loads_without_exception(self):
        event = Event(config_path=valid_config_path)


class TestEventRetrieve:
    def test_retrieve_event_name(self):
        assert valid_event.get_event_name() == 'name'

    def test_retrieve_event_start_time(self):
        assert valid_event.get_start_time() == 0

    def test_retrieve_event_end_time(self):
        assert valid_event.get_end_time() == 1

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
