import pytest
from charitybot2.botconfig.event_config import EventConfiguration, EventConfigurationCreator, EventConfigurationFromFile
from charitybot2.botconfig.json_config import InvalidConfigurationException, ConfigurationFileDoesNotExistException, \
    JSONConfigurationFile
from charitybot2.events.currency import InvalidCurrencyException
from tests.tests import TestFilePath


def get_valid_config_values():
    config_values = {}
    for key in EventConfigurationCreator.keys_required:
        config_values[key] = '' if key not in EventConfigurationCreator.number_keys else 0
    config_values['end_time'] = 1
    config_values['currency'] = 'GBP'
    config_values['source_url'] = 'http://www.test.com'
    return config_values


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

    # TODO: Update when refactoring how events handles names
    def test_passing_name_with_spaces_throws_exception(self):
        config_values = get_valid_config_values()
        config_values['event_name'] = 'bla bla bla bla bla'
        with pytest.raises(InvalidConfigurationException):
            EventConfigurationCreator(config_values)

    def test_passing_incorrect_currency_value_throws_exception(self):
        config_values = get_valid_config_values()
        config_values['currency'] = 'Hello'
        with pytest.raises(InvalidCurrencyException):
            EventConfigurationCreator(config_values)

    def test_passing_invalid_url_throws_exception(self):
        config_values = get_valid_config_values()
        config_values['source_url'] = 'this is a test'
        with pytest.raises(InvalidConfigurationException):
            EventConfigurationCreator(config_values)

    def test_passing_end_time_not_greater_than_start_time_throws_exception(self):
        config_values = get_valid_config_values()
        config_values['end_time'] = 0
        with pytest.raises(InvalidConfigurationException):
            EventConfigurationCreator(config_values)

    def test_getting_valid_event_configuration(self):
        event_config = EventConfigurationCreator(config_values=get_valid_config_values()).get_event_configuration()
        assert isinstance(event_config, EventConfiguration)


class TestEventConfigurationRetrieve:
    # This is just a sanity check... if this fails then something is very wrong
    def test_getting_event_config_values_match_passed_values(self):
        config_values = get_valid_config_values()
        event_config = EventConfigurationCreator(config_values=config_values).get_event_configuration()
        for key in EventConfigurationCreator.keys_required:
            assert config_values[key] == event_config.get_value(key)

    def test_getting_number_values_are_numbers(self):
        config_values = get_valid_config_values()
        event_config = EventConfigurationCreator(config_values=config_values).get_event_configuration()
        for key in EventConfigurationCreator.number_keys:
            assert isinstance(event_config.get_value(key), int)


class TestEventConfigurationFromFile:
    def test_passing_non_existent_file_throws_exception(self):
        with pytest.raises(ConfigurationFileDoesNotExistException):
            EventConfigurationFromFile(file_path='blalslsd')

    def test_getting_valid_event_configuration(self):
        config_file_path = TestFilePath().get_config_path('event', 'valid_config.json')
        event_config = EventConfigurationFromFile(file_path=config_file_path).get_event_configuration()
        assert isinstance(event_config, EventConfiguration)

    def test_event_config_values_match_values_from_file(self):
        config_file_path = TestFilePath().get_config_path('event', 'valid_config.json')
        event_config = EventConfigurationFromFile(file_path=config_file_path).get_event_configuration()
        json_config = JSONConfigurationFile(file_path=config_file_path, keys_required=EventConfigurationCreator.keys_required)
        for key in EventConfigurationCreator.keys_required:
            assert json_config.get_value(key) == event_config.get_value(key)
