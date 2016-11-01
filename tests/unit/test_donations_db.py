from charitybot2.events.donation import Donation
from charitybot2.storage.donations_db import DonationsDB
from neopysqlite.neopysqlite import Neopysqlite
from tests.tests import ResetDB, TestFilePath

donations_db_path = TestFilePath().get_db_path('donations.db')
donations_db_init_script_path = TestFilePath().get_db_path('donations.sql')


def setup_module():
    ResetDB(db_path=donations_db_path, sql_path=donations_db_init_script_path)


class TestDonationsDBInitialisation:
    def test_initialising_db(self):
        ddb = DonationsDB(db_path=donations_db_path, debug=True)


class TestDonationsDBRetrieve:
    def test_getting_all_donations_after_recording_one(self):
        ddb = DonationsDB(db_path=donations_db_path, debug=True)
        event_name = 'test_event_two'
        ddb.record_donation(event_name=event_name, donation=Donation(old_amount=500, new_amount=1000.1))
        recorded_donation = ddb.get_all_donations(event_name=event_name)[0]
        assert isinstance(recorded_donation, Donation)
        assert recorded_donation.get_donation_amount() == 500.1
        assert recorded_donation.get_new_amount() == 1000.1

    def test_event_existence_of_existing_event(self):
        ddb = DonationsDB(db_path=donations_db_path, debug=True)
        event_name = 'test_event_four'
        ddb.record_donation(event_name=event_name, donation=Donation(old_amount=500, new_amount=1000.1))
        assert True is ddb.event_exists(event_name=event_name)

    def test_getting_all_donations_after_recording_several(self):
        ddb = DonationsDB(db_path=donations_db_path, debug=True)
        event_name = 'test_event_three'
        old_amount = 0
        amount_increase = 50.34
        for i in range(5):
            ddb.record_donation(event_name=event_name, donation=Donation(old_amount=old_amount,
                                                                         new_amount=old_amount + amount_increase))
            old_amount += amount_increase
        new_amount = amount_increase
        all_donations = ddb.get_all_donations(event_name=event_name)
        for donation in all_donations:
            assert donation.get_donation_amount() == amount_increase
            assert donation.get_new_amount() == round(new_amount, 2)
            new_amount += amount_increase

    def test_getting_last_donation(self):
        ddb = DonationsDB(db_path=donations_db_path, debug=True)
        event_name = 'test_event_two'
        ddb.record_donation(event_name=event_name, donation=Donation(old_amount=300, new_amount=500))
        ddb.record_donation(event_name=event_name, donation=Donation(old_amount=500, new_amount=600))
        last_donation = ddb.get_last_donation(event_name=event_name)
        assert 100 == last_donation.get_donation_amount()
        assert 600 == last_donation.get_new_amount()

    def test_getting_average_donation_delta(self):
        ddb = DonationsDB(db_path=donations_db_path, debug=True)
        event_name = 'test_event_two'
        assert 266.7 == ddb.get_average_donation(event_name=event_name)


    def test_getting_event_names(self):
        ddb = DonationsDB(db_path=donations_db_path, debug=True)
        event_names = ('test', 'test_event_two', 'test_event_three', 'test_event_four')
        print(ddb.get_event_names())
        assert sorted(event_names) == sorted(ddb.get_event_names())


class TestDonationsDBRecording:
    def test_recording_donation_records_in_db(self):
        ddb = DonationsDB(db_path=donations_db_path, debug=True)
        donation = Donation(old_amount=533.3, new_amount=545.7)
        ddb.record_donation(event_name='test_event', donation=donation)
        db = Neopysqlite(database_name='Donations test DB', db_path=donations_db_path, verbose=True)
        all_donations = db.get_all_rows(table='test_event')
        assert len(all_donations) == 1
        assert all_donations[0][2] == 545.7
        delta = round(545.7 - 533.3, 2)
        assert all_donations[0][3] == delta


