import pytest
from charitybot2.models.donation import Donation
from charitybot2.services.donations_service import DonationsService

test_range = range(1, 6)
test_event_identifier = 'event'


def setup_test_donations(repository, test_range_values=test_range):
    donations = []
    for i in test_range_values:
        donations.append(
            Donation(amount=i, event_identifier=test_event_identifier, timestamp=i)
        )
    for donation in donations:
        repository.record_donation(donation=donation)


class TestDonationsService:
    donations_service = None

    def setup_method(self):
        self.donations_service = DonationsService(repository_path='memory')
        self.donations_service.open_connections()

    def teardown_method(self):
        self.donations_service.close_connections()

    def test_get_all_donations(self):
        setup_test_donations(self.donations_service._donations_repository)
        donations = self.donations_service.get_all_donations(
            event_identifier=test_event_identifier
        )
        assert len(test_range) == len(donations)
        for donation in donations:
            assert donation.amount in test_range
            assert donation.timestamp in test_range
            assert donation.event_identifier == test_event_identifier

    def test_get_all_donations_with_no_donations_present(self):
        donations = self.donations_service.get_all_donations(
            event_identifier=test_event_identifier
        )
        assert [] == donations
        assert 0 == len(donations)

    def test_get_latest_donation(self):
        setup_test_donations(self.donations_service._donations_repository)
        latest_donation = self.donations_service.get_latest_donation(test_event_identifier)
        assert test_range[-1] == latest_donation.amount
        assert test_range[-1] == latest_donation.timestamp
        assert test_event_identifier == latest_donation.event_identifier

    def test_get_latest_donation_with_no_donations_present(self):
        latest_donation = self.donations_service.get_latest_donation(
            event_identifier=test_event_identifier
        )
        assert None is latest_donation

    @pytest.mark.parametrize('limit', [
        1,
        2,
        3,
        4,
        5
    ])
    def get_latest_few_donations_given_a_limit(self, limit):
        setup_test_donations(self.donations_service._donations_repository)
        latest_donations = self.donations_service.get_latest_donations(
            event_identifier=test_event_identifier,
            limit=limit
        )
        assert isinstance(latest_donations, list)
        assert limit == len(latest_donations)
        for i in range(limit, 1, -1):
            assert i == latest_donations[i].amount
            assert i == latest_donations[i].timestamp
            assert test_event_identifier == latest_donations[i].event_identifer

    def test_get_largest_donation(self):
        decreasing_test_range = range(5, 1, -1)
        setup_test_donations(self.donations_service._donations_repository, test_range_values=decreasing_test_range)
        largest_donation = self.donations_service.get_largest_donation(
            event_identifier=test_event_identifier
        )
        assert decreasing_test_range[0] == largest_donation.amount
        assert decreasing_test_range[0] == largest_donation.timestamp
        assert test_event_identifier == largest_donation.event_identifier

    def test_get_largest_donation_with_no_donations_present(self):
        largest_donation = self.donations_service.get_largest_donation(
            event_identifier=test_event_identifier
        )
        assert None is largest_donation
