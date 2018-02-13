import pytest

from charitybot2.models.donation import Donation
from charitybot2.services.events_service import EventsService

test_range_min = 1
test_range_max = 6
test_range = range(test_range_min, test_range_max)
test_event_identifier = 'event'


def setup_test_donations(repository, test_range_values=test_range):
    donations = []
    for i in test_range_values:
        donations.append(
            Donation(amount=i, event_identifier=test_event_identifier, timestamp=i)
        )
    for donation in donations:
        repository.record_donation(donation=donation)


class TestEventsService:
    events_service = None

    def setup_method(self):
        self.events_service = EventsService(repository_path='memory')
        self.events_service.open_connections()

    def teardown_method(self):
        self.events_service.close_connections()

    def test_get_all_events(self):
        assert None is not None
