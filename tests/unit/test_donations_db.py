from charitybot2.events.donation import Donation
from charitybot2.storage.donations_db import DonationsDB
from neopysqlite.neopysqlite import Neopysqlite
from tests.tests import ResetDB, TestFilePath

donations_db_path = TestFilePath().get_db_path('donations.db')
donations_db_init_script_path = TestFilePath().get_db_path('donations.sql')

ResetDB(db_path=donations_db_path, sql_path=donations_db_init_script_path)


class TestDonationsDBInitialisation:
    def test_initialising_db(self):
        ddb = DonationsDB(db_path=donations_db_path, debug=True)


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


class TestDonationsDBRetrieve:
    def test_getting_all_donations_after_recording_one(self):
        ddb = DonationsDB(db_path=donations_db_path, debug=True)
        ddb.record_donation(event_name='test_event_two', donation=Donation(old_amount=500, new_amount=1000.1))
        recorded_donation = ddb.get_all_donations(event_name='test_event_two')[0]
        assert isinstance(recorded_donation, Donation)
        assert recorded_donation.get_donation_amount() == 500.1
        assert recorded_donation.get_new_amount() == 1000.1

    def test_getting_all_donations_after_recording_ten(self):
        ddb = DonationsDB(db_path=donations_db_path, debug=True)
        event_name = 'test_event_three'
        old_amount = 0
        amount_increase = 50.34
        for i in range(10):
            ddb.record_donation(event_name=event_name, donation=Donation(old_amount=old_amount, new_amount=old_amount + amount_increase))
            old_amount += amount_increase
        new_amount = amount_increase
        all_donations = ddb.get_all_donations(event_name=event_name)
        for donation in all_donations:
            assert donation.get_donation_amount() == amount_increase
            assert donation.get_new_amount() == round(new_amount, 2)
            new_amount += amount_increase
