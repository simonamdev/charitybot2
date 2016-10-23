import os

from charitybot2.events.donation import Donation
from charitybot2.storage.donations_db import DonationsDB
from neopysqlite.neopysqlite import Neopysqlite
from tests.tests import ResetDB

current_directory = os.path.dirname(os.path.abspath(__file__))
test_db_path = os.path.join(current_directory, 'db', 'test_donations.db')
test_db_init_script_path = os.path.join(current_directory, 'db', 'init_test_donations.sql')

ResetDB(db_path=test_db_path, sql_path=test_db_init_script_path)


class TestDonationsDBInitialisation:
    def test_initialising_db(self):
        ddb = DonationsDB(db_path=test_db_path, debug=True)

    def test_recording_donation_records_in_db(self):
        ddb = DonationsDB(db_path=test_db_path, debug=True)
        donation = Donation(old_amount=533.3, new_amount=545.7)
        ddb.record_donation(event='test_event', donation=donation)
        db = Neopysqlite(database_name='Donations test DB', db_path=test_db_path, verbose=True)
        all_donations = db.get_all_rows(table='test_event')
        print(all_donations)
        assert len(all_donations) == 1
        assert all_donations[0][2] == 545.7
        delta = round(545.7 - 533.3, 2)
        assert all_donations[0][3] == delta
