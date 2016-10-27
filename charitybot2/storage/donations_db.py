import time

from charitybot2.events.donation import Donation
from charitybot2.storage.base_db import BaseDB
from charitybot2.storage.logger import Logger


class DonationsDB(BaseDB):
    event_table_create_statement = 'CREATE TABLE `{}` (' \
                                   '`id`	    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,' \
                                   '`timestamp`	INTEGER NOT NULL,' \
                                   '`amount`	REAL NOT NULL,' \
                                   '`delta`	    REAL NOT NULL' \
                                   ');'

    def __init__(self, db_path, debug=False):
        super().__init__(file_path=db_path, db_name='Donations DB', verbose=debug)
        self.logger = Logger(source='Donations_DB', console_only=debug)

    def confirm_event_exists(self, event_name):
        if event_name not in self.db.get_table_names():
            self.logger.log_info('Creating table for event: {}'.format(event_name))
            self.db.execute_sql(self.event_table_create_statement.format(event_name))

    def record_donation(self, event_name, donation):
        self.confirm_event_exists(event_name=event_name)
        self.logger.log_info('Inserting donation: {} into donations database'.format(donation))
        self.db.insert_row(
            table=event_name,
            row_string='(NULL, ?, ?, ?)',
            row_data=(int(time.time()), donation.get_new_amount(), donation.get_donation_amount()))

    def get_all_donations(self, event_name):
        donation_rows = self.db.get_all_rows(table=event_name)
        return [Donation(old_amount=(row[2] - row[3]), new_amount=row[2]) for row in donation_rows]
