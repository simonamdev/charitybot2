from charitybot2.api.donations_api import donations_api, app, donations_api_identity
from charitybot2.api_calls.donations_api_wrapper import DonationsApiWrapper
from charitybot2.models.donation import Donation
from charitybot2.paths import donation_api_path
from charitybot2.start_service import Service, ServiceRunner
from helpers.event_config import get_test_event_configuration
from helpers.setup_test_database import setup_test_database

donations_api_wrapper = DonationsApiWrapper(base_url=donations_api.full_url)
test_event_identifier = get_test_event_configuration().identifier

service = Service(
    name='Donations Service',
    app=app,
    address='127.0.0.1',
    port=8001,
    debug=True)
service_runner = ServiceRunner(service=service, file_path=donation_api_path)

default_number_of_test_donations = 10
test_donations = []


def setup_module():
    global test_donations
    test_donations = setup_test_database(donation_count=default_number_of_test_donations)
    test_donations.reverse()  # Reverse to bring them into descending order
    service_runner.run()


def teardown_module():
    service_runner.stop_running()


class TestStartup:
    def test_getting_identity(self):
        response = donations_api_wrapper.get_index()
        assert isinstance(response['identity'], str)
        assert donations_api_identity == response['identity']
        assert isinstance(response['version'], int)
        assert 1 == response['version']
        assert True is response['debug']


class TestEventDonations:
    def test_retrieving_donations(self):
        donations = donations_api_wrapper.get_donations(event_identifier=test_event_identifier)
        assert default_number_of_test_donations == len(donations)
        for i in range(0, len(donations)):
            donation = donations[i]
            assert isinstance(donation, Donation)
            assert test_donations[i].internal_reference == donation.internal_reference

    def test_retrieving_donations_with_lower_bound(self):
        # find out the second donation's timestamp
        lower_timestamp = test_donations[2].timestamp
        donations = donations_api_wrapper.get_donations(
            event_identifier=test_event_identifier,
            lower_bound=lower_timestamp)
        expected_donation_count = 3
        assert expected_donation_count == len(donations)
        for i in range(0, expected_donation_count):
            donation = donations[i]
            assert isinstance(donation, Donation)
            assert test_donations[i].internal_reference == donation.internal_reference

