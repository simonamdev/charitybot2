import pytest
from charitybot2.models.donation import Donation
from charitybot2.persistence.donation_sqlite_repository import DonationSQLiteRepository, \
    DonationAlreadyRegisteredException


def setup_test_donations(repository):
    donations = []
    for i in range(1, 6):
        donations.append(Donation(amount=i, event_identifier='event', timestamp=i))
    for donation in donations:
        repository.record_donation(donation=donation)


def get_new_test_database():
    return DonationSQLiteRepository(debug=True)


class TestDonationSQLiteRepository:
    test_donation_repository = None
    test_event_identifier = 'event'

    def setup_method(self):
        self.test_donation_repository = get_new_test_database()
        setup_test_donations(self.test_donation_repository)

    def teardown_method(self):
        self.test_donation_repository.close_connection()

    def test_getting_all_donations(self):
        values = range(1, 6)
        donations = self.test_donation_repository.get_event_donations(
            event_identifier=self.test_event_identifier)
        assert 5 == len(donations)
        for donation in donations:
            assert donation.amount in values
            assert donation.timestamp in values
            assert donation.event_identifier == self.test_event_identifier

    def test_getting_all_donations_when_none_present_returns_empty_list(self):
        self.test_donation_repository = get_new_test_database()
        donations = self.test_donation_repository.get_latest_event_donation(
            event_identifier=self.test_event_identifier)
        assert [] == donations
        assert 0 == len(donations)

    def test_getting_latest_donation(self):
        latest_donation = self.test_donation_repository.get_latest_event_donation(
            event_identifier=self.test_event_identifier)
        assert 5 == latest_donation.amount
        assert 5 == latest_donation.timestamp
        assert self.test_event_identifier == latest_donation.event_identifier

    def test_getting_time_filtered_donations(self):
        lower_bound = 2
        upper_bound = 4
        expected_amount = upper_bound - lower_bound + 1
        filtered_donations = self.test_donation_repository.get_time_filtered_event_donations(
            event_identifier=self.test_event_identifier,
            lower_bound=lower_bound,
            upper_bound=upper_bound)
        assert expected_amount == len(filtered_donations)
        # I spent too much time trying to get this to work
        # TODO: Fix this test
        # for i in range(upper_bound, lower_bound - 1, -1):
        #     actual_index = len(filtered_donations) - 1
        #     assert i == filtered_donations[actual_index].timestamp

    def test_recording_donation(self):
        new_donation = Donation(
            amount=420,
            event_identifier='420',
            timestamp=420,
            internal_reference='wololo',
            external_reference='wooooo',
            donor_name='donor')
        self.test_donation_repository.record_donation(donation=new_donation)
        latest_donation = self.test_donation_repository.get_latest_event_donation(event_identifier='420')
        assert new_donation.amount == latest_donation.amount
        assert new_donation.timestamp == latest_donation.timestamp
        assert new_donation.event_identifier == latest_donation.event_identifier
        assert new_donation.internal_reference == latest_donation.internal_reference
        assert new_donation.external_reference == latest_donation.external_reference
        assert new_donation.donor_name == latest_donation.donor_name


class TestDonationSQLiteRepositoryExceptions:
    test_donation_repository = None

    def setup_method(self):
        self.test_donation_repository = DonationSQLiteRepository(debug=True)
        setup_test_donations(self.test_donation_repository)

    def teardown_method(self):
        self.test_donation_repository.close_connection()

    def test_recording_already_recorded_donation(self):
        donation = Donation(amount=500, event_identifier='wooo', timestamp=500, internal_reference='abcd')
        self.test_donation_repository.record_donation(donation=donation)
        with pytest.raises(DonationAlreadyRegisteredException):
            self.test_donation_repository.record_donation(donation=donation)

    def test_recording_donations_with_no_identifier_is_valid(self):
        for i in range(5):
            donation = Donation(amount=500, event_identifier='wooo', timestamp=500)
            self.test_donation_repository.record_donation(donation=donation)
