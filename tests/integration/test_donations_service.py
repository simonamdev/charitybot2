import pytest
from charitybot2.creators.event_configuration_creator import EventConfigurationCreator

from charitybot2.models.donation import Donation
from charitybot2.persistence.donation_sqlite_repository import DonationAlreadyRegisteredException
from charitybot2.persistence.event_sqlite_repository import EventNotRegisteredException
from charitybot2.services.donations_service import DonationsService

from helpers.event_config import get_updated_test_config_values


test_range_min = 1
test_range_max = 6
test_range = range(test_range_min, test_range_max)
test_event_identifier = 'donation_service_test_event'
test_currency_code = 'TST'
non_existent_event = 'blabalabla'


def get_test_event_config():
    test_config_values = get_updated_test_config_values(updated_values={'identifier': test_event_identifier})
    return EventConfigurationCreator(configuration_values=test_config_values).configuration


def register_test_event(service):
    service._event_repository.register_event(get_test_event_config())


def setup_test_donations(service, test_range_values=test_range):
    # Register donations
    donations = []
    for i in test_range_values:
        donations.append(
            Donation(
                amount=i,
                event_identifier=test_event_identifier,
                currency_code=test_currency_code,
                timestamp=i)
        )
    for donation in donations:
        service._donations_repository.record_donation(donation=donation)


class TestDonationsService:
    donations_service = None

    def setup_method(self):
        self.donations_service = DonationsService(repository_path='memory')
        self.donations_service.open_connections()
        # Register the test event
        register_test_event(self.donations_service)

    def teardown_method(self):
        self.donations_service.close_connections()

    def test_get_all_donations(self):
        setup_test_donations(self.donations_service)
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

    def test_get_all_donations_of_non_existent_event_throws_exception(self):
        with pytest.raises(EventNotRegisteredException):
            self.donations_service.get_all_donations(event_identifier=non_existent_event)

    def test_get_latest_donation(self):
        setup_test_donations(self.donations_service)
        latest_donation = self.donations_service.get_latest_donation(test_event_identifier)
        assert test_range[-1] == latest_donation.amount
        assert test_range[-1] == latest_donation.timestamp
        assert test_event_identifier == latest_donation.event_identifier

    def test_get_latest_donation_with_no_donations_present(self):
        latest_donation = self.donations_service.get_latest_donation(
            event_identifier=test_event_identifier
        )
        assert None is latest_donation

    def test_get_latest_donation_of_non_existent_event_throws_exception(self):
        with pytest.raises(EventNotRegisteredException):
            self.donations_service.get_latest_donation(event_identifier=non_existent_event)

    def test_get_number_of_latest_donations(self):
        setup_test_donations(self.donations_service)
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
        setup_test_donations(self.donations_service)
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

    def test_get_latest_donations_of_non_existent_event_throws_exception(self):
        with pytest.raises(EventNotRegisteredException):
            self.donations_service.get_latest_donations(event_identifier=non_existent_event, limit=5)

    def test_get_largest_donation(self):
        decreasing_test_range = range(5, 1, -1)
        setup_test_donations(self.donations_service, test_range_values=decreasing_test_range)
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

    def test_get_largest_donation_of_non_existent_event_throws_exception(self):
        with pytest.raises(EventNotRegisteredException):
            self.donations_service.get_largest_donation(event_identifier=non_existent_event)

    def test_get_average_donation(self):
        setup_test_donations(self.donations_service)
        # calculate average
        expected_average = sum(test_range) / len(test_range)
        actual_average = self.donations_service.get_average_donation(event_identifier=test_event_identifier)
        assert expected_average == actual_average

    def test_get_average_donation_with_no_donations_present(self):
        actual_average = self.donations_service.get_average_donation(event_identifier=test_event_identifier)
        assert 0.0 == actual_average

    def test_get_average_donation_of_non_existent_event_throws_exception(self):
        with pytest.raises(EventNotRegisteredException):
            self.donations_service.get_average_donation(event_identifier=non_existent_event)

    def test_get_time_bounded_donations_with_no_bounds_returns_all_donations(self):
        setup_test_donations(self.donations_service)
        donations = self.donations_service.get_time_bounded_donations(event_identifier=test_event_identifier)
        assert len(test_range) == len(donations)
        for i in range(test_range_max - 1, 0, -1):
            donation = donations[i - 1]
            value = test_range_max - i
            assert value == donation.amount
            assert value == donation.timestamp
            assert test_event_identifier == donation.event_identifier

    def test_get_time_bounded_donations_with_no_bounds_and_limit(self):
        setup_test_donations(self.donations_service)
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
        setup_test_donations(self.donations_service)
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
        setup_test_donations(self.donations_service)
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
        setup_test_donations(self.donations_service)
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
        setup_test_donations(self.donations_service)
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

    def test_get_time_bounded_donations_of_non_existent_event_throws_exception(self):
        with pytest.raises(EventNotRegisteredException):
            self.donations_service.get_time_bounded_donations(
                event_identifier=non_existent_event,
                lower_bound=2,
                upper_bound=5,
                limit=2)

    def test_get_number_of_donations_with_no_time_bounds(self):
        setup_test_donations(self.donations_service)
        assert len(test_range) == self.donations_service.get_number_of_donations(event_identifier=test_event_identifier)

    def test_get_number_of_donations_with_no_donations_present(self):
        assert 0 == self.donations_service.get_number_of_donations(event_identifier=test_event_identifier)

    def test_get_number_of_donations_with_lower_bound_only(self):
        setup_test_donations(self.donations_service)
        lower_bound = 2
        donation_count = self.donations_service.get_time_bounded_number_of_donations(
            event_identifier=test_event_identifier,
            lower_bound=lower_bound)
        assert test_range_max - lower_bound == donation_count

    def test_get_number_of_donations_with_upper_bound_only(self):
        setup_test_donations(self.donations_service)
        upper_bound = 3
        donation_count = self.donations_service.get_time_bounded_number_of_donations(
            event_identifier=test_event_identifier,
            upper_bound=upper_bound)
        assert upper_bound == donation_count

    def test_get_number_of_donations_with_time_bounds(self):
        setup_test_donations(self.donations_service)
        lower_bound = 2
        upper_bound = 4
        donation_count = self.donations_service.get_time_bounded_number_of_donations(
            event_identifier=test_event_identifier,
            lower_bound=lower_bound,
            upper_bound=upper_bound)
        assert upper_bound - lower_bound + 1 == donation_count

    def test_get_number_of_donations_of_non_existent_event_throws_exception(self):
        with pytest.raises(EventNotRegisteredException):
            self.donations_service.get_number_of_donations(event_identifier=non_existent_event)

    # Bounds: ((0, 10), (10, 20), (20, 50), (50, 75), (75, 100), (100, 10000))
    def test_donation_distribution(self):
        distribution_test_range = range(1, 999)
        setup_test_donations(self.donations_service, distribution_test_range)
        expected_distribution = [9, 10, 30, 25, 25, 899]
        actual_distribution = self.donations_service.get_donation_distribution(event_identifier=test_event_identifier)
        for i in range(0, len(expected_distribution)):
            assert expected_distribution[i] == actual_distribution[i]

    def test_donation_distribution_with_no_donations_present(self):
        expected_distribution = [0, 0, 0, 0, 0, 0]
        actual_distribution = self.donations_service.get_donation_distribution(event_identifier=test_event_identifier)
        for i in range(0, len(expected_distribution)):
            assert expected_distribution[i] == actual_distribution[i]

    def test_get_donation_distribution_of_non_existent_event_throws_exception(self):
        with pytest.raises(EventNotRegisteredException):
            self.donations_service.get_donation_distribution(event_identifier=non_existent_event)

    def test_registering_one_donation_with_no_donations_present(self):
        amount = 500.5
        timestamp = 555
        internal_reference = 'aaaa'
        external_reference = 'bbb'
        donor_name = 'bla'
        notes = 'Yo'
        donation = Donation(
            amount=amount,
            event_identifier=test_event_identifier,
            currency_code=test_currency_code,
            timestamp=timestamp,
            internal_reference=internal_reference,
            external_reference=external_reference,
            donor_name=donor_name,
            notes=notes)
        # Assert that no donations exist
        assert 0 == self.donations_service.get_number_of_donations(event_identifier=test_event_identifier)
        # Register the donation
        self.donations_service.register_donation(donation=donation)
        # Check that the donation exists
        assert 1 == self.donations_service.get_number_of_donations(event_identifier=test_event_identifier)
        donations = self.donations_service.get_all_donations(event_identifier=test_event_identifier)
        assert 1 == len(donations)
        stored_donation = donations[0]
        # Check the values
        assert amount == stored_donation.amount
        assert timestamp == stored_donation.timestamp
        assert internal_reference == stored_donation.internal_reference
        assert external_reference == stored_donation.external_reference
        assert donor_name == stored_donation.donor_name
        assert notes == stored_donation.notes

    def test_registering_several_donations_with_no_donations_present(self):
        setup_test_donations(self.donations_service, range(0, 0))
        number_of_donations = 5
        amount = 500.5
        timestamp = 555
        external_reference = 'bbb'
        donor_name = 'bla'
        notes = 'Yo'
        donations = []
        for i in range(0, number_of_donations):
            donation = Donation(
                amount=amount,
                event_identifier=test_event_identifier,
                currency_code=test_currency_code,
                timestamp=timestamp,
                internal_reference=str(i),
                external_reference=external_reference,
                donor_name=donor_name,
                notes=notes)
            donations.append(donation)
        assert 0 == self.donations_service.get_number_of_donations(event_identifier=test_event_identifier)
        amount = 0
        for i in range(0, number_of_donations):
            amount += 1
            self.donations_service.register_donation(donation=donations[i])
            assert amount == self.donations_service.get_number_of_donations(event_identifier=test_event_identifier)

    def test_registering_one_donation_with_donations_present(self):
        setup_test_donations(self.donations_service)
        amount = 500.5
        timestamp = 555
        internal_reference = 'aaaa'
        external_reference = 'bbb'
        donor_name = 'bla'
        notes = 'Yo'
        donation = Donation(
            amount=amount,
            event_identifier=test_event_identifier,
            currency_code=test_currency_code,
            timestamp=timestamp,
            internal_reference=internal_reference,
            external_reference=external_reference,
            donor_name=donor_name,
            notes=notes)
        # Assert that no donations exist
        assert len(test_range) == self.donations_service.get_number_of_donations(event_identifier=test_event_identifier)
        # Register the donation
        self.donations_service.register_donation(donation=donation)
        # Check that the donation exists
        assert len(test_range) + 1 == self.donations_service.get_number_of_donations(event_identifier=test_event_identifier)
        donations = self.donations_service.get_all_donations(event_identifier=test_event_identifier)
        assert len(test_range) + 1 == len(donations)
        stored_donation = donations[0]
        # Check the values
        assert amount == stored_donation.amount
        assert timestamp == stored_donation.timestamp
        assert internal_reference == stored_donation.internal_reference
        assert external_reference == stored_donation.external_reference
        assert donor_name == stored_donation.donor_name
        assert notes == stored_donation.notes

    def test_registering_several_donations_with_donations_present(self):
        setup_test_donations(self.donations_service)
        number_of_donations = 5
        amount = 500.5
        timestamp = 555
        external_reference = 'bbb'
        donor_name = 'bla'
        notes = 'Yo'
        donations = []
        for i in range(0, number_of_donations):
            donation = Donation(
                amount=amount,
                event_identifier=test_event_identifier,
                currency_code=test_currency_code,
                timestamp=timestamp,
                internal_reference=str(i),
                external_reference=external_reference,
                donor_name=donor_name,
                notes=notes)
            donations.append(donation)
        assert len(test_range) == self.donations_service.get_number_of_donations(event_identifier=test_event_identifier)
        amount = len(test_range)
        for i in range(0, number_of_donations):
            amount += 1
            self.donations_service.register_donation(donation=donations[i])
            assert amount == self.donations_service.get_number_of_donations(event_identifier=test_event_identifier)

    def test_registering_donation_already_registered_throws_exception(self):
        with pytest.raises(DonationAlreadyRegisteredException):
            amount = 500.5
            timestamp = 555
            internal_reference = 'aaaa'
            external_reference = 'bbb'
            donor_name = 'bla'
            notes = 'Yo'
            donation = Donation(
                amount=amount,
                event_identifier=test_event_identifier,
                currency_code=test_currency_code,
                timestamp=timestamp,
                internal_reference=internal_reference,
                external_reference=external_reference,
                donor_name=donor_name,
                notes=notes)
            # Register the donation
            self.donations_service.register_donation(donation=donation)
            # Register the donation again
            self.donations_service.register_donation(donation=donation)

    def test_registering_donation_of_non_existent_event_throws_exception(self):
        amount = 500.5
        timestamp = 555
        internal_reference = 'aaaa'
        external_reference = 'bbb'
        donor_name = 'bla'
        notes = 'Yo'
        donation = Donation(
            amount=amount,
            event_identifier=non_existent_event,
            currency_code=test_currency_code,
            timestamp=timestamp,
            internal_reference=internal_reference,
            external_reference=external_reference,
            donor_name=donor_name,
            notes=notes)
        with pytest.raises(EventNotRegisteredException):
            self.donations_service.register_donation(donation=donation)
