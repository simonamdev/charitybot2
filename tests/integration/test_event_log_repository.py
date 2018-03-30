from charitybot2.models.event_log import EventLog
from charitybot2.persistence.event_log_repository import EventLogRepository


test_event_identifier = 'test_event'


class TestEventLogRepository:
    test_event_log_repository = None

    def setup_method(self):
        self.test_event_log_repository = EventLogRepository(debug=True)

    def teardown_method(self):
        self.test_event_log_repository.close_connection()

    def test_retrieving_logged_events(self):
        logged_events = self.test_event_log_repository.get_logged_events()
        assert 0 == len(logged_events)
        # Add event log
        # TODO
        logged_events = self.test_event_log_repository.get_logged_events()
        assert 1 == len(logged_events)
        assert isinstance(logged_events[0], EventLog)
        assert test_event_identifier == logged_events[0].identifier
        test_event_log_time = 0
        assert test_event_log_time == logged_events[0].last_log_time

    def test_retrieving_logged_events_with_no_events_present(self):
        logged_events = self.test_event_log_repository.get_logged_events()
        assert 0 == len(logged_events)
