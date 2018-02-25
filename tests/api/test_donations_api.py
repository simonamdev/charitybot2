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

    def test_retrieving_donations_with_upper_bound(self):
        # find out the second donation's timestamp
        upper_timestamp = test_donations[2].timestamp
        donations = donations_api_wrapper.get_donations(
            event_identifier=test_event_identifier,
            upper_bound=upper_timestamp)
        excluded_donation_count = 2
        expected_donation_count = len(test_donations) - excluded_donation_count
        assert expected_donation_count == len(donations)
        for i in range(excluded_donation_count, expected_donation_count):
            donation = donations[i - excluded_donation_count]
            assert isinstance(donation, Donation)
            test_donation = test_donations[i]
            assert test_donation.internal_reference == donation.internal_reference

    def test_retrieving_donations_with_lower_and_upper_bound(self):
        # Choose timestamps
        upper_timestamp = test_donations[2].timestamp
        lower_timestamp = test_donations[4].timestamp
        expected_donation_count = 3
        donations = donations_api_wrapper.get_donations(
            event_identifier=test_event_identifier,
            lower_bound=lower_timestamp,
            upper_bound=upper_timestamp)
        assert expected_donation_count == len(donations)
        for i in range(upper_timestamp, lower_timestamp + 1):
            donation = donations[i - lower_timestamp]
            assert isinstance(donation, Donation)
            test_donation = test_donations[i]
            assert test_donation.internal_reference == donation.internal_reference

    def test_retrieving_donations_with_lower_and_upper_bound_and_limit(self):
        # Choose timestamps
        upper_timestamp = test_donations[2].timestamp
        lower_timestamp = test_donations[4].timestamp
        expected_donation_count = 2
        donations = donations_api_wrapper.get_donations(
            event_identifier=test_event_identifier,
            lower_bound=lower_timestamp,
            upper_bound=upper_timestamp,
            limit=expected_donation_count)
        assert expected_donation_count == len(donations)
        for i in range(upper_timestamp, lower_timestamp + 1):
            donation = donations[i - lower_timestamp]
            assert isinstance(donation, Donation)
            test_donation = test_donations[i]
            assert test_donation.internal_reference == donation.internal_reference

    def test_retrieving_latest_donation(self):
        latest_donation = donations_api_wrapper.get_latest_donation(event_identifier=test_event_identifier)
        assert isinstance(latest_donation, Donation)
        assert test_donations[0].internal_reference == latest_donation.internal_reference

    def test_retrieving_number_of_donations(self):
        actual_count = donations_api_wrapper.get_number_of_donations(event_identifier=test_event_identifier)
        assert isinstance(actual_count, int)
        assert default_number_of_test_donations == actual_count

    def test_retrieving_number_of_donations_with_lower_bound(self):
        lower_timestamp = test_donations[2].timestamp
        expected_donation_count = 3
        actual_count = donations_api_wrapper.get_number_of_donations(
            event_identifier=test_event_identifier,
            lower_bound=lower_timestamp)
        assert isinstance(actual_count, int)
        assert expected_donation_count == actual_count

    def test_retrieving_number_of_donations_with_upper_bound(self):
        upper_timestamp = test_donations[2].timestamp
        excluded_donation_count = 2
        expected_donation_count = default_number_of_test_donations - excluded_donation_count
        actual_count = donations_api_wrapper.get_number_of_donations(
            event_identifier=test_event_identifier,
            upper_bound=upper_timestamp)
        assert isinstance(actual_count, int)
        assert expected_donation_count == actual_count

    def test_retrieving_number_of_donations_with_lower_bound_and_upper_bound(self):
        upper_timestamp = test_donations[2].timestamp
        lower_timestamp = test_donations[4].timestamp
        expected_donation_count = 3
        actual_count = donations_api_wrapper.get_number_of_donations(
            event_identifier=test_event_identifier,
            lower_bound=lower_timestamp,
            upper_bound=upper_timestamp)
        assert isinstance(actual_count, int)
        assert expected_donation_count == actual_count

    def test_get_average_donation_amount(self):
        expected_average_donation_amount = sum(
            [donation.amount for donation in test_donations]
        ) / default_number_of_test_donations
        actual_average_donation_amount = donations_api_wrapper.get_average_donation_amount(event_identifier=test_event_identifier)
        assert round(expected_average_donation_amount, 2) == round(actual_average_donation_amount, 2)
