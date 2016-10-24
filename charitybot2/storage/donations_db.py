import time
from charitybot2.storage.base_db import BaseDB
from charitybot2.storage.logger import Logger


class DonationsDB(BaseDB):
    event_table_create_statement = 'CREATE TABLE `{}` (' \
                                   '`id`	    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,' \
                                   '`timestamp`	INTEGER NOT NULL UNIQUE,' \
                                   '`amount`	REAL NOT NULL UNIQUE,' \
                                   '`delta`	    REAL NOT NULL UNIQUE' \
                                   ');'

    def __init__(self, db_path, debug=False):
        super().__init__(file_path=db_path, db_name='Donations DB', verbose=debug)
        self.logger = Logger(source='Donations DB', console_only=debug)

    def confirm_event_exists(self, event):
        if event not in self.db.get_table_names():
            self.logger.log_info('Creating table for event: {}'.format(event))
            self.db.execute_sql(self.event_table_create_statement.format(event))

    def record_donation(self, event, donation):
        self.confirm_event_exists(event=event)
        self.logger.log_info('Inserting donation: {} into donations database'.format(donation))
        self.db.insert_row(
            table=event,
            row_string='(NULL, ?, ?, ?)',
            row_data=(int(time.time()), donation.get_new_amount(), donation.get_donation_amount()))


