from charitybot2.models.donation import Donation
from charitybot2.services.donations_service import DonationsService

test_range = range(1, 6)
test_event_identifier = 'event'


def setup_test_donations(repository):
    donations = []
    for i in test_range:
        donations.append(Donation(amount=i, event_identifier='event', timestamp=i))
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

    def test_get_latest_donations(self):
        setup_test_donations(self.donations_service._donations_repository)
        latest_donation = self.donations_service.get_latest_donation(test_event_identifier)
        assert test_range[-1] == latest_donation.amount
        assert test_range[-1] == latest_donation.timestamp
        assert test_event_identifier == latest_donation.event_identifier
