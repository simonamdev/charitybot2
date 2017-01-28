import pytest
from charitybot2.configurations.event_configuration import EventConfiguration

test_configuration_values = {
    'identifier': 'identifier',
    'title': 'This is a Title',
    'start_time': 0,
    'end_time': 1,
    'target_amount': 100,
    'update_delay': 5,
    'currency_key': 'EUR'
}
test_event_configuration = EventConfiguration(configuration_values=test_configuration_values)


class TestEventConfigurationInstantiation:
    @pytest.mark.parametrize('expected,actual', [

    ])
    def test_retrieval(self, expected, actual):
        pass
