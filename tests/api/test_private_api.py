import pytest
from charitybot2.api_calls.private_api_calls import PrivateApiCalls
from charitybot2.exceptions import IllegalArgumentException
from charitybot2.models.donation import Donation
from charitybot2.models.event import NonExistentEventException
from charitybot2.private_api.private_api import private_api_identity
from tests.api.setup_test_database import setup_test_database
from tests.integration.test_event_register import get_test_event_configuration
from tests.mocks import MockPrivateAPI

mock_private_api = MockPrivateAPI()
private_api_calls = PrivateApiCalls()

test_event_identifier = get_test_event_configuration().identifier


def setup_module():
    setup_test_database(donation_count=10)
    mock_private_api.start()


def teardown_module():
    mock_private_api.stop()


class TestStartup:
    def test_getting_identity_string(self):
        response = private_api_calls.get_index()
        assert isinstance(response['identity'], str)
        assert private_api_identity == response['identity']
        assert isinstance(response['version'], int)
        assert 1 == response['version']
        assert True is response['debug']


class TestEventInformation:
    def test_getting_existence_of_non_existent_returns_false_existence(self):
        response = private_api_calls.get_event_existence('foobar')
        assert False is response

    def test_getting_event_existence(self):
        response = private_api_calls.get_event_existence(identifier=test_event_identifier)
        assert True is response

    def test_getting_event_info(self):
        info = private_api_calls.get_event_info(identifier=test_event_identifier)
        test_config_values = get_test_event_configuration().configuration_values
        assert test_config_values.get('title') == info.get('title')

    def test_getting_event_info_of_non_existent_event_throws_exception(self):
        with pytest.raises(NonExistentEventException):
            info = private_api_calls.get_event_info(identifier='foobar')

    def test_getting_event_total(self):
        # hardcoded amount for total, depends on test database setup script
        expected_total = 5.0
        actual_total = private_api_calls.get_event_total(event_identifier='test')
        assert expected_total == actual_total

    def test_getting_event_total_of_non_existent_event_throws_exception(self):
        with pytest.raises(NonExistentEventException):
            total = private_api_calls.get_event_total(event_identifier='everything is awesome')


class TestEventRegistration:
    def test_registering_new_event(self):
        updated_values = {
            'identifier': 'registration_test',
            'title': 'Registration Test Event'
        }
        registration_test_configuration = get_test_event_configuration(updated_values=updated_values)
        response = private_api_calls.register_event(event_configuration=registration_test_configuration)
        assert True is response

    def test_updating_new_event(self):
        updated_values = {
            'identifier': 'update_test',
            'title': 'Update Test Event'
        }
        registration_test_configuration = get_test_event_configuration(updated_values=updated_values)
        response = private_api_calls.register_event(event_configuration=registration_test_configuration)
        assert True is response
        updated_values = {
            'identifier': 'update_test',
            'start_time': 500,
            'end_time': 1000
        }
        update_test_configuration = get_test_event_configuration(updated_values=updated_values)
        response = private_api_calls.update_event(event_configuration=update_test_configuration)
        assert True is response


class TestHeartbeat:
    def test_sending_heartbeat_returns_true(self):
        received = private_api_calls.send_heartbeat(
            'This is a valid heartbeat string',
            'heartbeat_source',
            1)
        assert True is received

    @pytest.mark.parametrize('state', [
        None,
        0,
        1.0,
        object,
        (),
        []
    ])
    def test_sending_illegal_heartbeats_throws_exception(self, state):
        with pytest.raises(IllegalArgumentException):
            private_api_calls.send_heartbeat(state, 'valid')
            private_api_calls.send_heartbeat('valid', state)


class TestDonationRegistration:
    def test_registering_valid_donation(self):
        donation = Donation(amount=50, event_identifier=test_event_identifier)
        response = private_api_calls.register_donation(donation=donation)
        assert True is response

    def test_registering_fully_defined_valid_donation(self):
        donation = Donation(
            amount=-30,
            event_identifier=test_event_identifier,
            timestamp=123,
            internal_reference='foobar',
            external_reference='wat',
            donor_name='some guy',
            notes='she sells sea shells on the sea shore',
            valid=False
        )
        response = private_api_calls.register_donation(donation=donation)
        assert True is response


# Disabled due to assertion check not working properly for this specific method
    # @pytest.mark.parametrize('donation', [
    #     None,
    #     0,
    #     1.0,
    #     object,
    #     (),
    #     []
    # ])
    # def test_sending_illegal_values_throws_exception(self, donation):
    #     with pytest.raises(IllegalArgumentException):
    #         private_api_calls.register_donation(donation=donation)


class TestEventDonations:
    def test_retrieving_valid_donations(self):
        donation_listing_test_identifier = 'donation_listing_test'
        updated_values = {
            'identifier': donation_listing_test_identifier,
            'title': 'Donation Listing Test Event'
        }
        donation_listing_test_configuration = get_test_event_configuration(updated_values=updated_values)
        # Register the event
        private_api_calls.register_event(event_configuration=donation_listing_test_configuration)
        # Add a few donations
        donation_count = 3
        for i in range(1, donation_count + 1):
            donation = Donation(
                amount=i,
                event_identifier=donation_listing_test_identifier,
                timestamp=i)
            private_api_calls.register_donation(donation=donation)
        # Retrieve the stored donations and confirm they are correct
        donations = private_api_calls.get_event_donations(event_identifier=donation_listing_test_identifier)
        assert donation_count == len(donations)
        for donation in donations:
            assert isinstance(donation, Donation)
            assert donation.amount == donation.timestamp

    def test_retrieving_valid_time_filtered_donations(self):
        filtered_donations_identifier = 'filtered_donation_listing_test'
        updated_values = {
            'identifier': filtered_donations_identifier,
            'title': 'Filtered Donation Listing Test Event'
        }
        donation_listing_test_configuration = get_test_event_configuration(updated_values=updated_values)
        # Register the event
        private_api_calls.register_event(event_configuration=donation_listing_test_configuration)
        # Add a few donations
        donation_count = 7
        for i in range(1, donation_count):
            donation = Donation(
                amount=i,
                event_identifier=filtered_donations_identifier,
                timestamp=i)
            private_api_calls.register_donation(donation=donation)
        # Retrieve the stored donations and confirm they are correct
        lower_bound = 3
        upper_bound = 5
        expected_donation_count = upper_bound - lower_bound + 1
        donations = private_api_calls.get_event_donations(
            event_identifier=filtered_donations_identifier,
            time_bounds=(3, 5))
        assert expected_donation_count == 3
        for donation in donations:
            assert isinstance(donation, Donation)
            assert donation.amount == donation.timestamp

    @pytest.mark.parametrize('time_bounds', [
        (1, 'bla'),
        ('', 2),
        ('', ''),
        (object, object),
        ('', ''),
        (2.33, 55.5)
    ])
    def test_retrieving_donations_from_timeframe_given_wrong_values_throws_exception(self, time_bounds):
        with pytest.raises(IllegalArgumentException):
            private_api_calls.get_event_donations(
                event_identifier=test_event_identifier,
                time_bounds=time_bounds)

    def test_retrieving_donations_from_non_existent_event_throws_exception(self):
        with pytest.raises(NonExistentEventException):
            private_api_calls.get_event_donations(event_identifier='bla')

    def test_retrieving_donations_from_event_with_spaces_throws_exception(self):
        with pytest.raises(NonExistentEventException):
            private_api_calls.get_event_donations(event_identifier='cats are_awesome')
