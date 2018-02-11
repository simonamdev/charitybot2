import pytest
from charitybot2.models.donation import Donation
from charitybot2.services.donations_service import DonationsService

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

    def test_get_number_of_latest_donations(self):
        setup_test_donations(self.donations_service._donations_repository)
        limit = 3
        latest_donations = self.donations_service.get_latest_donations(test_event_identifier, limit=limit)
        for i in range(0, limit):
            donation = latest_donations[i]
            value = test_range_max - 1 - i
            assert value == donation.amount
            assert value == donation.timestamp
            assert test_event_identifier == donation.event_identifier

    def test_get_number_of_latest_donations_with_no_donations_present(self):
        limit = 3
        latest_donations = self.donations_service.get_latest_donations(test_event_identifier, limit=limit)
        assert 0 == len(latest_donations)

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

    def test_get_average_donation(self):
        setup_test_donations(self.donations_service._donations_repository)
        # calculate average
        expected_average = sum(test_range) / len(test_range)
        actual_average = self.donations_service.get_average_donation(event_identifier=test_event_identifier)
        assert expected_average == actual_average

    def test_get_average_donation_with_no_donations_present(self):
        actual_average = self.donations_service.get_average_donation(event_identifier=test_event_identifier)
        assert 0.0 == actual_average

    def test_get_time_bounded_donations_with_no_bounds_returns_all_donations(self):
        setup_test_donations(self.donations_service._donations_repository)
        donations = self.donations_service.get_time_bounded_donations(event_identifier=test_event_identifier)
        assert len(test_range) == len(donations)
        for i in range(test_range_max - 1, 0, -1):
            donation = donations[i - 1]
            value = test_range_max - i
            assert value == donation.amount
            assert value == donation.timestamp
            assert test_event_identifier == donation.event_identifier

    def test_get_time_bounded_donations_with_no_bounds_and_limit(self):
        setup_test_donations(self.donations_service._donations_repository)
        limit = 3
        donations = self.donations_service.get_time_bounded_donations(
            event_identifier=test_event_identifier,
            limit=limit)
        assert limit == len(donations)
        for i in range(0, limit):
            donation = donations[i]
            value = test_range_max - 1 - i
            assert value == donation.amount
            assert value == donation.timestamp
            assert test_event_identifier == donation.event_identifier

    def test_get_time_bounded_donations_with_lower_bound_only(self):
        setup_test_donations(self.donations_service._donations_repository)
        lower_bound = 2
        donations = self.donations_service.get_time_bounded_donations(
            event_identifier=test_event_identifier,
            lower_bound=lower_bound)
        assert test_range_max - lower_bound == len(donations)
        for i in range(0, test_range_max - lower_bound):
            donation = donations[i]
            value = test_range_max - i - 1
            assert value == donation.amount
            assert value == donation.timestamp
            assert test_event_identifier == donation.event_identifier

    def test_get_time_bounded_donations_with_upper_bound_only(self):
        setup_test_donations(self.donations_service._donations_repository)
        upper_bound = 4
        donations = self.donations_service.get_time_bounded_donations(
            event_identifier=test_event_identifier,
            upper_bound=upper_bound)
        assert upper_bound == len(donations)
        for i in range(0, upper_bound):
            donation = donations[i]
            value = upper_bound - i
            assert value == donation.amount
            assert value == donation.timestamp
            assert test_event_identifier == donation.event_identifier

    def test_get_time_bounded_donations_with_both_bounds(self):
        setup_test_donations(self.donations_service._donations_repository)
        lower_bound = 2
        upper_bound = 4
        donations = self.donations_service.get_time_bounded_donations(
            event_identifier=test_event_identifier,
            lower_bound=lower_bound,
            upper_bound=upper_bound)
        assert upper_bound - lower_bound + 1 == len(donations)
        for i in range(0, upper_bound - lower_bound + 1):
            donation = donations[i]
            value = upper_bound - i
            assert value == donation.amount
            assert value == donation.timestamp
            assert test_event_identifier == donation.event_identifier

    def test_get_time_bounded_donations_with_both_bounds_and_limit(self):
        setup_test_donations(self.donations_service._donations_repository)
        limit = 2
        lower_bound = 2
        upper_bound = 5
        donations = self.donations_service.get_time_bounded_donations(
            event_identifier=test_event_identifier,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            limit=limit)
        assert limit == len(donations)
        for i in range(0, limit):
            donation = donations[i]
            value = upper_bound - i
            assert value == donation.amount
            assert value == donation.timestamp
            assert test_event_identifier == donation.event_identifier

    def test_get_time_bounded_donations_with_no_donations_present(self):
        limit = 2
        lower_bound = 2
        upper_bound = 5
        donations = self.donations_service.get_time_bounded_donations(
            event_identifier=test_event_identifier,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            limit=limit)
        assert 0 == len(donations)
