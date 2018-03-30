import pytest
from charitybot2.configurations.event_configuration import EventConfiguration
from charitybot2.configurations.justgiving_event_configuration import JustGivingEventConfiguration
from helpers.event_config import test_event_config_values, test_justgiving_event_config_values

test_event_configuration = EventConfiguration(configuration_values=test_event_config_values)


class TestEventConfiguration:
    @pytest.mark.parametrize('expected,actual', [
        (test_event_config_values['identifier'], test_event_configuration.identifier),
        (test_event_config_values['title'], test_event_configuration.title),
        (test_event_config_values['start_time'], test_event_configuration.start_time),
        (test_event_config_values['end_time'], test_event_configuration.end_time),
        (test_event_config_values['target_amount'], test_event_configuration.target_amount),
        (test_event_config_values['update_delay'], test_event_configuration.update_delay),
        (test_event_config_values['currency_key'], test_event_configuration.currency.key),
        (test_event_config_values['source_details']['source'], test_event_configuration.source),
        (test_event_config_values['source_details']['url'], test_event_configuration.source_url),
        (test_event_config_values, test_event_configuration.configuration_values)
    ])
    def test_retrieval(self, expected, actual):
        assert expected == actual

test_justgiving_event_configuration = JustGivingEventConfiguration(configuration_values=test_justgiving_event_config_values)


class TestJustGivingEventConfiguration:
    @pytest.mark.parametrize('expected,actual', [
        (test_justgiving_event_config_values['source_details']['source'], test_justgiving_event_configuration.source),
        (test_justgiving_event_config_values['source_details']['url'], test_justgiving_event_configuration.source_url),
        (test_justgiving_event_config_values['source_details']['page_short_name'], test_justgiving_event_configuration.page_short_name),
        (test_justgiving_event_config_values, test_justgiving_event_configuration.configuration_values)
    ])
    def test_retrieval(self, expected, actual):
        assert expected == actual
