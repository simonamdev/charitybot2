import pytest
from charitybot2.botconfig.event_config import EventConfiguration, InvalidEventNameException, EventConfigurationCreator
from charitybot2.botconfig.json_config import InvalidConfigurationException
from charitybot2.events.currency import InvalidCurrencyException
from tests.tests import TestFilePath
#
#
# def get_config_file_path(config_name):
#     return TestFilePath().get_config_path('event', config_name + '.json')
#
#
# class TestEventConfigExistence:
#     def test_event_config_does_exist(self):
#         ec = EventConfiguration(file_path=get_config_file_path('valid_config'))
#         assert ec.config_exists() is True
#
#
# class TestEventConfigRetrieve:
#     def test_source_url_is_valid_url(self):
#         import re
#         url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
#         ec = EventConfiguration(file_path=get_config_file_path('valid_config'))
#         source_url = ec.get_value('source_url')
#         urls = re.findall(url_regex, source_url)
#         assert len(urls) == 1
#
#     def test_retrieve_integers_when_getting_integer_related_keys(self):
#         ec = EventConfiguration(file_path=get_config_file_path('valid_config'))
#         for key in EventConfiguration.number_keys:
#             assert isinstance(ec.get_value(key), int)
#
#     def test_currency_is_of_expected_type(self):
#         ec = EventConfiguration(file_path=get_config_file_path('valid_config'))
#         assert 'GBP' == ec.get_value('currency')
#
#
# class TestEventConfigValidity:
#     def test_passing_wrong_currency_throws_exception(self):
#         with pytest.raises(InvalidCurrencyException):
#             ec = EventConfiguration(file_path=get_config_file_path('bad_currency'))
#
#     def test_passing_event_name_with_spaces_throws_exception(self):
#         with pytest.raises(InvalidEventNameException):
#             ec = EventConfiguration(file_path=get_config_file_path('name_with_spaces'))


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
        config_values = {}
        for key in EventConfigurationCreator.keys_required:
            config_values[key] = '' if key not in EventConfigurationCreator.number_keys else 0
        config_values['currency'] = 'GBP'
        config_values['event_name'] = 'bla bla bla bla bla'
        with pytest.raises(InvalidEventNameException):
            EventConfigurationCreator(config_values)

    def test_passing_incorrect_currency_value_throws_exception(self):
        config_values = {}
        for key in EventConfigurationCreator.keys_required:
            config_values[key] = '' if key not in EventConfigurationCreator.number_keys else 0
        with pytest.raises(InvalidCurrencyException):
            EventConfigurationCreator(config_values)

    def test_getting_valid_event_configuration(self):
        config_values = {}
        for key in EventConfigurationCreator.keys_required:
            config_values[key] = '' if key not in EventConfigurationCreator.number_keys else 0
        config_values['currency'] = 'GBP'
        event_config = EventConfigurationCreator(config_values=config_values).get_event_configuration()
        assert isinstance(event_config, EventConfiguration)
