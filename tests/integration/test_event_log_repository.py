from charitybot2.persistence.event_log_repository import EventLogRepository


class TestEventLogRepository:
    test_event_log_repository = None

    def setup_method(self):
        self.test_event_log_repository = EventLogRepository(debug=True)

    def teardown_method(self):
        self.test_event_log_repository.close_connection()

    def test_retrieving_logged_events(self):
        assert None is not None

    def test_retrieving_logged_events_with_no_events_present(self):
        assert None is not None
