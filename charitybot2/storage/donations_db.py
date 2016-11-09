import time

from charitybot2.events.donation import Donation
from charitybot2.storage.base_db import BaseDB
from charitybot2.storage.logger import Logger


def convert_row_to_donation(row):
    return Donation(old_amount=(row[2] - row[3]), new_amount=row[2], timestamp=row[1])


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

    def record_donation(self, event_name, donation):
        self.create_event_table_if_not_exists(event_name=event_name)
        self.logger.log_info('Inserting donation: {} into donations database'.format(donation))
        self.db.insert_row(
            table=event_name,
            row_string='(NULL, ?, ?, ?)',
            row_data=(int(time.time()), donation.get_new_amount(), donation.get_donation_amount()))

    def create_event_table_if_not_exists(self, event_name):
        if not self.event_exists(event_name=event_name):
            self.logger.log_info('Creating table for event: {}'.format(event_name))
            self.db.execute_sql(self.event_table_create_statement.format(event_name))

    def event_exists(self, event_name):
        return event_name in self.db.get_table_names()

    def get_all_donations(self, event_name):
        donation_rows = self.db.get_all_rows(table=event_name)
        return [convert_row_to_donation(row) for row in donation_rows]

    def get_last_donation(self, event_name):
        # Need to implement get last row in neopysqlite, luckily performance isn't such an issue
        return self.get_all_donations(event_name=event_name)[-1]

    def get_average_donation(self, event_name):
        donations = self.get_all_donations(event_name=event_name)
        donation_deltas = [donation.get_donation_amount() for donation in donations]
        return round(sum(donation_deltas) / len(donation_deltas), 2)

    def get_event_names(self):
        names_to_remove = ('sqlite_sequence', 'currency')
        return [name for name in self.db.get_table_names() if name not in names_to_remove]

    def get_event_currency_key(self, event_name):
        currency_key = self.db.get_specific_rows(table='currency', filter_string='event = \'{}\''.format(event_name))
        return currency_key[0][2]

    def set_event_currency_key(self, event_name, currency_key):
        self.db.insert_row(table='currency', row_string='(NULL, ?, ?)', row_data=(event_name, currency_key))
