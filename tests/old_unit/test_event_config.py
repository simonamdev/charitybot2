import pytest
from charitybot2.botconfig.event_config import EventConfiguration, EventConfigurationCreator, EventConfigurationFromFile
from charitybot2.botconfig.json_config import InvalidConfigurationException, ConfigurationFileDoesNotExistException
from charitybot2.events.currency import InvalidCurrencyException, Currency
from tests.paths_for_tests import valid_config_path


def get_valid_config_values():
    config_values = {}
    for key in EventConfigurationCreator.keys_required:
        config_values[key] = '' if key not in EventConfigurationCreator.number_keys else 0
    config_values['internal_name'] = 'internal_name'
    config_values['external_name'] = 'External Name'
    config_values['end_time'] = 1
    config_values['target_amount'] = 1000
    config_values['currency_key'] = 'GBP'
    config_values['source_url'] = 'http://www.test.com'
    config_values['update_delay'] = 5
    return config_values

valid_event_config = EventConfigurationCreator(config_values=get_valid_config_values()).get_event_configuration()


class TestEventConfigCreator:
    def test_not_passing_all_required_keys_throws_exception(self):
        with pytest.raises(InvalidConfigurationException):
            EventConfigurationCreator({'foo': 5, 'bla': 3, 'fizz': 'buzz'})

    def test_passing_incorrect_formatted_values_throws_exception(self):
        config_values = {}
        for key in EventConfigurationCreator.keys_required:
            config_values[key] = ''
        with pytest.raises(InvalidConfigurationException):
            EventConfigurationCreator(config_values)

    @pytest.mark.parametrize('key,value', [
        ('internal_name', 'this should not have spaces'),
        ('currency_key',  'definitely not a currency'),
        ('source_url',    'definitely not a URL'),
        ('end_time',      0),
        ('end_time',      -1)
    ])
    def test_passing_invalid_values_throws_exception(self, key, value):
        config_values = get_valid_config_values()
        config_values[key] = value
        with pytest.raises(InvalidConfigurationException):
            EventConfigurationCreator(config_values=config_values)

    def test_getting_valid_event_configuration(self):
        event_config = EventConfigurationCreator(config_values=get_valid_config_values()).get_event_configuration()
        assert isinstance(event_config, EventConfiguration)


class TestEventConfigurationRetrieval:
    @pytest.mark.parametrize('number_value', [
        valid_event_config.get_start_time(),
        valid_event_config.get_end_time(),
        valid_event_config.get_target_amount(),
        valid_event_config.get_update_delay()
    ])
    def test_getting_number_values_are_numbers(self, number_value):
        assert isinstance(number_value, int)

    @pytest.mark.parametrize('expected_value,actual_value', [
        ('internal_name',       valid_event_config.get_internal_name()),
        ('External Name',       valid_event_config.get_external_name()),
        (0,                     valid_event_config.get_start_time()),
        (1,                     valid_event_config.get_end_time()),
        (1000,                  valid_event_config.get_target_amount()),
        ('http://www.test.com', valid_event_config.get_source_url()),
        (5,                     valid_event_config.get_update_delay())
    ])
    def test_value_retrieval(self, expected_value, actual_value):
        assert expected_value == actual_value

    def test_event_returns_expected_currency(self):
        assert isinstance(valid_event_config.get_currency(), Currency)
        assert 'GBP' == valid_event_config.get_currency().get_key()
        assert '£' == valid_event_config.get_currency().get_symbol()


class TestEventConfigurationFromFile:
    def test_passing_non_existent_file_throws_exception(self):
        with pytest.raises(ConfigurationFileDoesNotExistException):
            EventConfigurationFromFile(file_path='blalslsd')

    def test_getting_valid_event_configuration(self):
        event_config = EventConfigurationFromFile(file_path=valid_config_path).get_event_configuration()
        assert isinstance(event_config, EventConfiguration)

