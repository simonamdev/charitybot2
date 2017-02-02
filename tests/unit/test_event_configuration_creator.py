import copy

import pytest
from charitybot2.configurations.event_configuration import EventConfiguration
from charitybot2.creators.event_configuration_creator import EventConfigurationCreator, \
    InvalidEventConfigurationException, EventConfigurationCreatorFromFile
from tests.paths_for_tests import valid_event_config_path
from tests.unit.test_event_configuration import test_event_configuration_values


def get_updated_test_config_values(updated_values):
    valid_config_values = copy.deepcopy(test_event_configuration_values)
    valid_config_values.update(updated_values)
    return valid_config_values

test_event_configuration = EventConfiguration(configuration_values=test_event_configuration_values)
test_event_configuration_creator = EventConfigurationCreator(configuration_values=test_event_configuration_values)


class TestEventConfigurationCreator:
    @pytest.mark.parametrize('configuration_values', [
        {},
        {'foo': 'bar'},
        (),
        None,
        'test',
        123,
        get_updated_test_config_values(updated_values={'currency_key': 'Zimbabwe Dollars'}),
        get_updated_test_config_values(updated_values={'start_time': 1, 'end_time': 0}),
        get_updated_test_config_values(updated_values={'start_time': -300, 'end_time': 1}),
        get_updated_test_config_values(updated_values={'start_time': -20, 'end_time': -10}),
        get_updated_test_config_values(updated_values={'identifier': 'this cannot have spaces'}),
        get_updated_test_config_values(updated_values={'identifier': ''}),
        get_updated_test_config_values(updated_values={'title': ''}),
        get_updated_test_config_values(updated_values={'start_time': 'never'}),
        get_updated_test_config_values(updated_values={'end_time': 'heat death of the universe'}),
        get_updated_test_config_values(updated_values={'source_url': 'htt definitely not a url'})
    ])
    def test_passing_incorrect_values_throws_exception(self, configuration_values):
        with pytest.raises(InvalidEventConfigurationException):
            EventConfigurationCreator(configuration_values=configuration_values)

    @pytest.mark.parametrize('expected,actual', [
        (test_event_configuration_creator.configuration.identifier, test_event_configuration.identifier),
        (test_event_configuration_creator.configuration.title, test_event_configuration.title),
        (test_event_configuration_creator.configuration.start_time, test_event_configuration.start_time),
        (test_event_configuration_creator.configuration.end_time, test_event_configuration.end_time),
        (test_event_configuration_creator.configuration.currency.key, test_event_configuration.currency.key),
        (test_event_configuration_creator.configuration.target_amount, test_event_configuration.target_amount),
        (test_event_configuration_creator.configuration.source_url, test_event_configuration.source_url),
        (test_event_configuration_creator.configuration.update_delay, test_event_configuration.update_delay),
    ])
    def test_retrieving_values_match_passed_values_to_creator(self, expected, actual):
        assert expected == actual

    def test_retrieving_event_configuration_from_creator(self):
        event_configuration_creator = EventConfigurationCreator(configuration_values=test_event_configuration_values)
        assert isinstance(event_configuration_creator.configuration, EventConfiguration)

test_event_configuration_creator_from_file = EventConfigurationCreatorFromFile(file_path=valid_event_config_path)


class TestEventConfigurationCreatorFromFile:
    @pytest.mark.parametrize('file_path', [
        '',
        'bla'
    ])
    def test_passing_incorrect_file_paths_throw_exception(self, file_path):
        with pytest.raises(FileNotFoundError):
            EventConfigurationCreatorFromFile(file_path=file_path)

    @pytest.mark.parametrize('expected,actual', [
        (test_event_configuration_creator_from_file.configuration.identifier, test_event_configuration.identifier),
        (test_event_configuration_creator_from_file.configuration.title, test_event_configuration.title),
        (test_event_configuration_creator_from_file.configuration.start_time, test_event_configuration.start_time),
        (test_event_configuration_creator_from_file.configuration.end_time, test_event_configuration.end_time),
        (test_event_configuration_creator_from_file.configuration.currency.key, test_event_configuration.currency.key),
        (test_event_configuration_creator_from_file.configuration.target_amount, test_event_configuration.target_amount),
        (test_event_configuration_creator_from_file.configuration.source_url, test_event_configuration.source_url),
        (test_event_configuration_creator_from_file.configuration.update_delay, test_event_configuration.update_delay)
    ])
    def test_passing_valid_file_path_values_match_valid_values(self, expected, actual):
        assert expected == actual
