import pytest
from charitybot2.configurations.event_configuration import EventConfiguration

test_event_config_values = {
    'identifier': 'test',
    'title': 'CB Test Event',
    'start_time': 0,
    'end_time': 1,
    'target_amount': 100,
    'update_delay': 5,
    'currency_key': 'EUR',
    'source_url': 'http://www.charitybot.net'
}
test_event_configuration = EventConfiguration(configuration_values=test_event_config_values)


class TestEventConfigurationInstantiation:
    @pytest.mark.parametrize('expected,actual', [
        (test_event_config_values['identifier'], test_event_configuration.identifier),
        (test_event_config_values['title'], test_event_configuration.title),
        (test_event_config_values['start_time'], test_event_configuration.start_time),
        (test_event_config_values['end_time'], test_event_configuration.end_time),
        (test_event_config_values['target_amount'], test_event_configuration.target_amount),
        (test_event_config_values['update_delay'], test_event_configuration.update_delay),
        (test_event_config_values['currency_key'], test_event_configuration.currency.key),
        (test_event_config_values['source_url'], test_event_configuration.source_url),
        (test_event_config_values, test_event_configuration.configuration_values)
    ])
    def test_retrieval(self, expected, actual):
        assert expected == actual
