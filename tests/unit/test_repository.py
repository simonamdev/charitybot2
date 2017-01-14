import pytest
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


class TestDonationsDBRetrieve:
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
        event_configuration = EventConeve
        repository.register_event()
        assert repository.event_exists('i_like_cats')

    def test_registering_event_with_spaces_in_name_throws_exception(self):
        with pytest.raises(EventInvalidException):
            repository.register_event()

    def test_getting_all_donations_after_recording_several(self):
        event_name = 'test_event_three'
        old_amount = 0
        amount_increase = 50.34
        for i in range(5):
            repository.record_donation(
                event_name=event_name,
                donation=Donation(old_amount=old_amount, new_amount=old_amount + amount_increase))
            old_amount += amount_increase
        new_amount = amount_increase
        all_donations = repository.get_all_donations(event_name=event_name)
        for donation in all_donations:
            assert donation.get_donation_amount() == amount_increase
            assert donation.get_total_raised() == round(new_amount, 2)
            new_amount += amount_increase

    def test_getting_last_donation(self):
        event_name = 'test_event_two'
        donations_db.record_donation(event_name=event_name, donation=Donation(old_amount=300, new_amount=500))
        donations_db.record_donation(event_name=event_name, donation=Donation(old_amount=500, new_amount=600))
        last_donation = donations_db.get_last_donation(event_name=event_name)
        assert 100 == last_donation.get_donation_amount()
        assert 600 == last_donation.get_total_raised()

    def test_getting_average_donation_delta(self):
        event_name = 'test_event_two'
        assert 266.7 == donations_db.get_average_donation(event_name=event_name)

    def test_getting_event_names(self):
        event_names = ('test', 'test_event_two', 'test_event_three', 'test_event_four')
        assert sorted(event_names) == sorted(donations_db.get_event_names())

    def test_get_donations_from_a_timespan(self):
        last_timespan_donations = donations_db.get_donations_for_timespan(event_name='test', timespan_start=1477258100)
        assert 6 == len(last_timespan_donations)

    def test_get_largest_donation(self):
        largest_donation = donations_db.get_largest_donation(event_name='test')
        assert 42 == largest_donation.get_donation_amount()
        assert 1477258844 == largest_donation.get_timestamp()


class TestDonationsDBRecording:
    def test_recording_donation_records_in_db(self):
        donation = Donation(old_amount=533.3, new_amount=545.7)
        donations_db.record_donation(event_name='test_event', donation=donation)
        all_donations = donations_db.get_all_donations(event_name='test_event')
        assert 1 == len(all_donations)
        assert 545.7 == all_donations[0].get_total_raised()
        assert round(545.7 - 533.3, 2) == all_donations[0].get_donation_amount()
