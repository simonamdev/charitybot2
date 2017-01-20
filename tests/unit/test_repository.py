import pytest
import time
from charitybot2.botconfig.event_config import EventConfigurationFromFile, EventConfigurationCreator
from charitybot2.events.donation import Donation
from charitybot2.events.event import Event
from charitybot2.storage.repository import Repository, EventNotRegisteredException
from tests.mocks import ResetDB
from tests.paths_for_tests import TestFilePath

repository_db_path = TestFilePath().get_repository_db_path()
repository_script_path = TestFilePath().get_repository_script_path()
repository = Repository(db_path=repository_db_path, debug=True)

event_names = (
    'TestOne',
    'TestTwo',
    'TestThree',
    'TestFour',
    'valid_configured_event',
    'NoDonations',
    'LastOneInvalid',
    'OnlyInvalid')


def setup_module():
    ResetDB(db_path=repository_db_path, sql_path=repository_script_path)


class TestRepositoryInitialisation:
    def test_initialising_db(self):
        repository = Repository(db_path=repository_db_path, debug=True)


class TestRepositoryOperations:
    def test_getting_event_ids(self):
        assert 1 == repository.get_event_id(event_name='TestOne')
        assert 2 == repository.get_event_id(event_name='TestTwo')
        assert 3 == repository.get_event_id(event_name='TestThree')

    def test_getting_event_id_of_non_existent_event_throws_exception(self):
        with pytest.raises(EventNotRegisteredException):
            repository.get_event_id(event_name='meowmeow')

    def test_getting_number_of_donations(self):
        assert 5 == repository.get_number_of_donations(event_name='TestOne')

    def test_donations_are_present(self):
        assert True is repository.donations_are_present(event_name='TestOne')
        assert False is repository.donations_are_present(event_name='NoDonations')

    def test_get_last_4_donations(self):
        event_name = 'TestOne'
        last_4_donations = repository.get_donations(event_name=event_name, amount=4)
        assert 4 == len(last_4_donations)
        assert 63.17 == last_4_donations[0].get_donation_amount()
        assert 1477257000 == last_4_donations[0].get_timestamp()

    def test_get_last_donations_given_amount_0_or_negative_returns_all(self):
        event_name = 'TestOne'
        last_donations = repository.get_donations(event_name=event_name)
        all_donations = repository.get_all_donations(event_name=event_name)
        assert len(last_donations) == len(all_donations)
        for i in range(0, len(last_donations)):
            assert last_donations[i].get_donation_amount() == all_donations[i].get_donation_amount()
            assert last_donations[i].get_total_raised() == all_donations[i].get_total_raised()
            assert last_donations[i].get_timestamp() == all_donations[i].get_timestamp()
            assert last_donations[i].get_validity() == all_donations[i].get_validity()
            assert last_donations[i].get_notes() == all_donations[i].get_notes()

    def test_getting_all_donations(self):
        donations = repository.get_all_donations(event_name='TestTwo')
        for donation in donations:
            assert isinstance(donation, Donation)
        assert 10.0 == donations[0].get_donation_amount()
        assert 30.0 == donations[0].get_total_raised()
        assert 1477257010 == donations[0].get_timestamp()

    def test_getting_all_donations_after_recording_one(self):
        event_name = 'TestThree'
        repository.record_donation(event_name=event_name, donation=Donation(old_amount=3300.0, new_amount=3400.0))
        recorded_donation = repository.get_all_donations(event_name=event_name)[0]
        assert isinstance(recorded_donation, Donation)
        assert 100.0 == recorded_donation.get_donation_amount()
        assert 3400.0 == recorded_donation.get_total_raised()

    def test_event_existence_of_existing_event(self):
        assert True is repository.event_exists(event_name='TestThree')

    def test_event_existence_of_non_existent_event(self):
        assert False is repository.event_exists(event_name='meow')

    def test_registering_new_event(self):
        config_file_path = TestFilePath().get_config_path('event', 'valid_config.json')
        event_configuration = EventConfigurationFromFile(file_path=config_file_path).get_event_configuration()
        repository.register_event(event_configuration=event_configuration)
        assert repository.event_exists('valid_configured_event')

    def test_retrieving_event_configuration(self):
        event_configuration = repository.get_event_configuration(event_name='TestOne')
        event = Event(event_configuration=event_configuration, db_path=repository_db_path)
        assert 'TestOne' == event.name
        assert 'Test One Title' == event_configuration.get_external_name()
        assert 1477256983 == event_configuration.get_start_time()
        assert 1477256985 == event_configuration.get_end_time()
        assert 'GBP' == event_configuration.get_currency().get_key()
        assert 1000 == event_configuration.get_target_amount()
        assert 5 == event_configuration.get_update_delay()
        assert 'http://127.0.0.1:5000/justgiving' == event_configuration.get_source_url()

    def test_updating_event_configuration(self):
        config_file_path = TestFilePath().get_config_path('event', 'valid_config.json')
        event_config_data = EventConfigurationFromFile(file_path=config_file_path).get_config_data()
        event_config_data['end_time'] = 888888888888888
        event_configuration = EventConfigurationCreator(config_values=event_config_data).get_event_configuration()
        repository.update_event(event_configuration=event_configuration)
        new_configuration = repository.get_event_configuration('valid_configured_event')
        assert 888888888888888 == new_configuration.get_end_time()

    def test_getting_donations_after_recording_several(self):
        event_name = 'TestTwo'
        amount_to_add = 5
        old_amount = 0
        amount_increase = 50.34
        timestamp = int(time.time())
        for i in range(amount_to_add):
            timestamp += 2
            repository.record_donation(
                event_name=event_name,
                donation=Donation(old_amount=old_amount, new_amount=old_amount + amount_increase, timestamp=timestamp))
            old_amount += amount_increase
        new_amount = amount_increase
        new_donations = repository.get_donations(event_name=event_name, amount=amount_to_add)
        new_donations.reverse()
        for donation in new_donations:
            assert donation.get_donation_amount() == amount_increase
            assert donation.get_total_raised() == round(new_amount, 2)
            new_amount += amount_increase

    def test_getting_last_donation(self):
        event_name = 'TestOne'
        current_time = int(time.time())
        repository.record_donation(
            event_name=event_name,
            donation=Donation(old_amount=100, new_amount=200, timestamp=current_time))
        repository.record_donation(
            event_name=event_name,
            donation=Donation(old_amount=200, new_amount=350, timestamp=current_time + 5))
        last_donation = repository.get_last_donation(event_name=event_name)
        assert isinstance(last_donation, Donation)
        assert 150 == last_donation.get_donation_amount()
        assert 350 == last_donation.get_total_raised()

    def test_getting_starting_amount(self):
        event_name = 'NoDonations'
        starting_amount = repository.get_starting_amount(event_name=event_name)
        assert isinstance(starting_amount, float)
        assert 100 == starting_amount

    def test_getting_last_donation_when_no_donations_present_returns_starting_amount(self):
        event_name = 'NoDonations'
        starting_amount = repository.get_last_donation(event_name=event_name)
        assert starting_amount == repository.get_starting_amount(event_name=event_name)

    def test_getting_last_invalid_donation_returns_closest_valid_donation_instead(self):
        event_name = 'LastOneInvalid'
        last_donation = repository.get_last_donation(event_name=event_name)
        assert True is last_donation.get_validity()
        assert 50 == last_donation.get_donation_amount()
        assert 150 == last_donation.get_total_raised()
        assert 1477257104 == last_donation.get_timestamp()

    def test_getting_last_invalid_donation(self):
        event_name = 'LastOneInvalid'
        last_invalid_donation = repository.get_last_donation(event_name=event_name, get_invalid=True)
        assert False is last_invalid_donation.get_validity()
        assert -100 == last_invalid_donation.get_donation_amount()
        assert 50 == last_invalid_donation.get_total_raised()
        assert 1477257114 == last_invalid_donation.get_timestamp()

    def test_getting_total_raised(self):
        # test where last donation is valid
        assert 150 == repository.get_total_raised('TestFour')
        # test where last donation is invalid
        assert 50 == repository.get_total_raised('LastOneInvalid')
        assert 0 == repository.get_total_raised('OnlyInvalid')

    def test_getting_average_donation_amount(self):
        event_name = 'TestThree'
        assert 100 == repository.get_average_donation(event_name=event_name)

    def test_getting_average_donation_amount_does_not_include_invalid_donations(self):
        event_name = 'TestFour'
        assert 87.5 == repository.get_average_donation(event_name=event_name)

    def test_getting_zero_average_donation_with_no_donations_present(self):
        event_name = 'NoDonations'
        average_donation = repository.get_average_donation(event_name=event_name)
        assert isinstance(average_donation, float)
        assert 0.0 == average_donation

    def test_getting_event_names(self):
        assert sorted(event_names) == sorted(repository.get_event_names())

    def test_get_donations_from_a_timespan(self):
        last_timespan_donations = repository.get_donations_for_timespan(
            event_name='TestFour',
            timespan_start=1477257061)
        assert 2 == len(last_timespan_donations)

    def test_get_largest_donation(self):
        largest_donation = repository.get_largest_donation(event_name='TestFour')
        assert 100 == largest_donation.get_donation_amount()
        assert 1477257070 == largest_donation.get_timestamp()

    def test_getting_largest_donation_returns_none_when_no_donations_are_present(self):
        largest_donation = repository.get_largest_donation(event_name='NoDonations')
        assert largest_donation is None

    def test_getting_donation_regressions(self):
        event_name = 'LastOneInvalid'
        regressions = repository.get_donation_regressions(event_name=event_name, amount=1)
        assert 1 == len(regressions)
        assert -100 == regressions[0].get_donation_amount()
        assert 50 == regressions[0].get_total_raised()
        assert 1477257114 == regressions[0].get_timestamp()
        assert 'Regression' == regressions[0].get_notes()
        assert False is regressions[0].get_validity()
        regressions = repository.get_donation_regressions(event_name='OnlyInvalid')
        assert 2 == len(regressions)

    def test_recording_donation_regression(self):
        event_name = 'LastOneInvalid'
        regression = Donation(
            old_amount=50,
            new_amount=25.5,
            timestamp=int(time.time()),
            notes='Regression Test',
            valid=False)
        repository.record_donation(event_name=event_name, donation=regression)
        regressions = repository.get_donation_regressions(event_name=event_name)
        assert 2 == len(regressions)
        assert regression.get_donation_amount() == regressions[0].get_donation_amount()
        assert regression.get_total_raised() == regressions[0].get_total_raised()
        assert regression.get_timestamp() == regressions[0].get_timestamp()
        assert regression.get_notes() == regressions[0].get_notes()
        assert regression.get_validity() is regressions[0].get_validity()

