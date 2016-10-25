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
