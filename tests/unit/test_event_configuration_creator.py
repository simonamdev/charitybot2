import copy

import pytest
from charitybot2.creators.event_configuration_creator import InvalidEventConfigurationException, \
    EventConfigurationCreator
from tests.unit.test_event_configuration import test_event_configuration_values


def get_updated_test_config_values(updated_values):
    valid_config_values = copy.deepcopy(test_event_configuration_values)
    valid_config_values.update(updated_values)
    return valid_config_values


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
