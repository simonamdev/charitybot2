from charitybot2.events.donation import Donation
from charitybot2.storage.repository import Repository
from neopysqlite.neopysqlite import Neopysqlite
from tests.tests import ResetDB, TestFilePath

donations_db_path = TestFilePath().get_db_path('donations.db')
donations_db_init_script_path = TestFilePath().get_db_path('donations.sql')
donations_db = Repository(db_path=donations_db_path, debug=True)


def setup_module():
    ResetDB(db_path=donations_db_path, sql_path=donations_db_init_script_path)


class TestRepositoryInitialisation:
    def test_initialising_db(self):
        ddb = Repository(db_path=donations_db_path, debug=True)


class TestDonationsDBRetrieve:
    def test_getting_number_of_donations(self):
        assert 15 == donations_db.get_number_of_donations(event_name='test')

    def test_getting_all_donations_after_recording_one(self):
        event_name = 'test_event_two'
        donations_db.record_donation(event_name=event_name, donation=Donation(old_amount=500, new_amount=1000.1))
        recorded_donation = donations_db.get_all_donations(event_name=event_name)[0]
        assert isinstance(recorded_donation, Donation)
        assert recorded_donation.get_donation_amount() == 500.1
        assert recorded_donation.get_total_raised() == 1000.1

    def test_event_existence_of_existing_event(self):
        event_name = 'test_event_four'
        donations_db.record_donation(event_name=event_name, donation=Donation(old_amount=500, new_amount=1000.1))
        assert True is donations_db.event_exists(event_name=event_name)

    def test_getting_all_donations_after_recording_several(self):
        event_name = 'test_event_three'
        old_amount = 0
        amount_increase = 50.34
        for i in range(5):
            donations_db.record_donation(event_name=event_name, donation=Donation(old_amount=old_amount, new_amount=old_amount + amount_increase))
            old_amount += amount_increase
        new_amount = amount_increase
        all_donations = donations_db.get_all_donations(event_name=event_name)
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
