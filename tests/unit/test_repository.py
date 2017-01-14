import pytest
from charitybot2.botconfig.event_config import EventConfigurationFromFile, EventConfigurationCreator
from charitybot2.events.donation import Donation
from charitybot2.events.event import EventInvalidException
from charitybot2.storage.repository import Repository, EventNotRegisteredException
from tests.tests import ResetDB, TestFilePath

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
        repository.record_donation(event_name=event_name, donation=Donation(old_amount=100, new_amount=200))
        repository.record_donation(event_name=event_name, donation=Donation(old_amount=200, new_amount=350))
        last_donation = repository.get_last_donation(event_name=event_name)
        assert 150 == last_donation.get_donation_amount()
        assert 350 == last_donation.get_total_raised()

    def test_getting_average_donation_amount(self):
        event_name = 'TestThree'
        assert 100 == repository.get_average_donation(event_name=event_name)

    def test_getting_average_donation_amount_does_not_include_invalid_donations(self):
        event_name = 'TestFour'
        assert 87.5 == repository.get_average_donation(event_name=event_name)

    def test_getting_event_names(self):
        event_names = ('TestOne', 'TestTwo', 'TestThree', 'TestFour', 'valid_configured_event')
        assert sorted(event_names) == sorted(repository.get_event_names())

    def test_get_donations_from_a_timespan(self):
        last_timespan_donations = repository.get_donations_for_timespan(
            event_name='TestFour',
            timespan_start=1477257061)
        assert 1 == len(last_timespan_donations)

    def test_get_largest_donation(self):
        largest_donation = repository.get_largest_donation(event_name='TestFour')
        assert 100 == largest_donation.get_donation_amount()
        assert 1477257060 == largest_donation.get_timestamp()
