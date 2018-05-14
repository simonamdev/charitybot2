import random

import pytest
from charitybot2.models.event_log import EventLog
from charitybot2.persistence.event_log_repository import EventLogRepository, EventLogAlreadyExistsException, \
    EventLogDoesNotExistException

test_event_identifier = 'test_event'
non_existent_event_identifier = 'blalbalblabla'
test_event_log_time = 123


class TestEventLogRepository:
    test_event_log_repository = None

    def setup_method(self):
        self.test_event_log_repository = EventLogRepository(debug=True)

    def teardown_method(self):
        self.test_event_log_repository.close_connection()

    def test_check_if_non_existent_event_log_exists(self):
        assert False is self.test_event_log_repository.event_log_exists(event_identifier=non_existent_event_identifier)

    def test_check_if_existing_event_log_exists(self):
        self.test_event_log_repository.add_event_log(
            event_identifier=test_event_identifier,
            timestamp=test_event_log_time
        )
        assert True is self.test_event_log_repository.event_log_exists(event_identifier=test_event_identifier)

    def test_retrieving_logged_events(self):
        logged_events = self.test_event_log_repository.get_logged_events()
        assert 0 == len(logged_events)
        self.test_event_log_repository.add_event_log(
            event_identifier=test_event_identifier,
            timestamp=test_event_log_time
        )
        logged_events = self.test_event_log_repository.get_logged_events()
        assert 1 == len(logged_events)
        assert isinstance(logged_events[0], EventLog)
        assert test_event_identifier == logged_events[0].identifier
        assert test_event_log_time == logged_events[0].last_log_time

    def test_retrieving_logged_events_with_no_events_present(self):
        logged_events = self.test_event_log_repository.get_logged_events()
        assert 0 == len(logged_events)

    def test_adding_new_event_log(self):
        new_event_log_event_identifier = 'new_event'
        assert False is self.test_event_log_repository.event_log_exists(event_identifier=new_event_log_event_identifier)
        self.test_event_log_repository.add_event_log(
            event_identifier=new_event_log_event_identifier,
            timestamp=test_event_log_time)
        assert True is self.test_event_log_repository.event_log_exists(event_identifier=new_event_log_event_identifier)

    def test_adding_new_event_log_when_it_already_exists(self):
        existing_event_log_event_identifier = 'this_event_already exists'
        existing_time = test_event_log_time + random.randint(5, 10)
        self.test_event_log_repository.add_event_log(
            event_identifier=existing_event_log_event_identifier,
            timestamp=existing_time
        )
        with pytest.raises(EventLogAlreadyExistsException):
            self.test_event_log_repository.add_event_log(
                event_identifier=existing_event_log_event_identifier,
                timestamp=existing_time
            )

    def test_updating_existing_event_log(self):
        event_log_being_updated_identifier = 'I am Being Updooted'
        self.test_event_log_repository.add_event_log(
            event_identifier=event_log_being_updated_identifier,
            timestamp=test_event_log_time
        )
        new_time = test_event_log_time + random.randint(100, 200)
        self.test_event_log_repository.update_event_log(
            event_identifier=event_log_being_updated_identifier,
            timestamp=new_time
        )
        assert new_time == self.test_event_log_repository.get_event_log_timestamp(
            event_identifier=event_log_being_updated_identifier
        )

    def test_updating_non_existent_event_log(self):
        with pytest.raises(EventLogDoesNotExistException):
            self.test_event_log_repository.update_event_log(
                event_identifier=non_existent_event_identifier,
                timestamp=1010101001
            )
