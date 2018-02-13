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

    def test_get_all_event_identifiers(self):
        assert None is not None

    def test_get_all_event_identifiers_with_no_events_returns_empty_list(self):
        assert None is not None

    def test_existing_event_is_registered(self):
        assert None is not None

    def test_non_existent_event_is_not_registered(self):
        assert None is not None

    def test_retrieving_existing_event_configuration(self):
        assert None is not None

    def test_retrieving_non_existent_event_configuration_throws_exception(self):
        assert None is not None

    def test_register_event(self):
        assert None is not None

    def test_registering_already_registered_event_throws_exceptions(self):
        assert None is not None

    def test_registering_event_with_invalid_values_throws_exception(self):
        assert None is not None

    def test_updating_existing_event(self):
        assert None is not None

    def test_updating_non_existent_event_throws_exception(self):
        assert None is not None

    def test_updating_event_with_invalid_values_throws_exception(self):
        assert None is not None

    def test_setting_event_total(self):
        assert None is not None

    def test_setting_non_existent_event_total_throws_exception(self):
        assert None is not None
