import pytest
from charitybot2.models.event_log import EventLog

test_event_identifier = 'test_event'
test_event_log_time = 500
test_event_log = EventLog(
    event_identifier=test_event_identifier,
    last_log_time=test_event_log_time
)


class TestEventLog:
    @pytest.mark.parametrize('expected,actual', [
        (test_event_identifier, test_event_log.identifier),
        (test_event_log_time, test_event_log.last_log_time)
    ])
    def test_event_log_values(self, expected, actual):
        assert expected == actual
