import pytest
from charitybot2.configurations.event_configuration import EventConfiguration
from charitybot2.models.event import Event
from tests.unit.test_event_configuration import test_event_configuration_values

test_event_configuration = EventConfiguration(configuration_values=test_event_configuration_values)
test_event = Event(configuration=test_event_configuration)


class TestEventInstantiation:
    @pytest.mark.parametrize('expected,actual', [
        (test_event_configuration, test_event.configuration),
        ('identifier', test_event.configuration.identifier),
        ('This is a Title', test_event.configuration.title),
        (0, test_event.configuration.start_time),
        (1, test_event.configuration.end_time),
        (5, test_event.configuration.update_delay),
        (test_event_configuration.currency.key, test_event.configuration.currency.key),
        (0, test_event.amount_raised),
        (0, test_event.starting_amount)
    ])
    def test_retrieval(self, expected, actual):
        assert expected == actual
