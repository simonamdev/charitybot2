import pytest
import time
from charitybot2.botconfig.event_config import EventConfigurationFromFile, EventConfigurationCreator
from charitybot2.events.donation import Donation
from charitybot2.events.event import Event
from charitybot2.storage.repository import Repository, EventNotRegisteredException
from tests.restters_for_tests import ResetDB, TestFilePath

repository_db_path = TestFilePath().get_repository_db_path()
repository_script_path = TestFilePath().get_repository_script_path()
repository = Repository(db_path=repository_db_path, debug=True)


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

    def test_getting_all_donations(self):
        donations = repository.get_all_donations(event_name='TestTwo')
        for donation in donations:
            assert isinstance(donation, Donation)
        assert -10.0 == donations[2].get_donation_amount()
        assert 20.0 == donations[2].get_total_raised()
        assert "Mistake" == donations[2].get_notes()

    def test_getting_all_donations_after_recording_one(self):
        repository.record_donation(event_name='TestThree', donation=Donation(old_amount=3300.0, new_amount=3400.0))
        recorded_donation = repository.get_all_donations(event_name='TestThree')[-1]
        assert isinstance(recorded_donation, Donation)
        assert recorded_donation.get_donation_amount() == 100.0
        assert recorded_donation.get_total_raised() == 3400.0

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
        assert 'TestOne' == event.get_internal_name()
        assert 'Test One Title' == event.get_external_name()
        assert 1477256983 == event.get_start_time()
        assert 1477256985 == event.get_end_time()
        assert 'GBP' == event.get_currency().get_key()
        assert 1000 == event.get_target_amount()
        assert 5 == event.get_update_tick()

    def test_updating_event_configuration(self):
        config_file_path = TestFilePath().get_config_path('event', 'valid_config.json')
        event_config_data = EventConfigurationFromFile(file_path=config_file_path).get_config_data()
        event_config_data['end_time'] = 888888888888888
        event_configuration = EventConfigurationCreator(config_values=event_config_data).get_event_configuration()
        repository.update_event(event_configuration=event_configuration)
        new_configuration = repository.get_event_configuration('valid_configured_event')
        event = Event(event_configuration=new_configuration, db_path=repository_db_path)
        assert 888888888888888 == event.get_end_time()

    def test_getting_all_donations_after_recording_several(self):
        event_name = 'TestTwo'
        old_amount = 0
        amount_increase = 50.34
        already_stored_count = repository.get_number_of_donations(event_name=event_name)
        for i in range(5):
            repository.record_donation(
                event_name=event_name,
                donation=Donation(old_amount=old_amount, new_amount=old_amount + amount_increase))
            old_amount += amount_increase
        new_amount = amount_increase
        all_donations = repository.get_all_donations(event_name=event_name)
        new_donations = all_donations[already_stored_count:-1]
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
        print(last_donation)
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
        print(last_donation)
        assert True is last_donation.get_validity()
        assert 50 == last_donation.get_donation_amount()
        assert 150 == last_donation.get_total_raised()
        assert 1477257104 == last_donation.get_timestamp()

    def test_getting_last_invalid_donation(self):
        event_name = 'LastOneInvalid'
        last_invalid_donation = repository.get_last_donation(event_name=event_name, get_invalid=True)
        print(last_invalid_donation)
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

    def test_getting_event_names(self):
        event_names = (
            'TestOne',
            'TestTwo',
            'TestThree',
            'TestFour',
            'valid_configured_event',
            'NoDonations',
            'LastOneInvalid',
            'OnlyInvalid')
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
