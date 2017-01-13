import time

from charitybot2.events.donation import Donation
from charitybot2.storage.logger import Logger


def convert_row_to_donation(row):
    return Donation(old_amount=(row[2] - row[3]), new_amount=row[2], timestamp=row[1])


class Repository:
    def __init__(self, db_path, debug=False):
        super().__init__(file_path=db_path, db_name='Donations DB', verbose=debug)
        self.logger = Logger(source='Donations_DB', event='', console_only=debug)

    def get_number_of_donations(self, event_name):
        return_row = self.db.get_specific_rows(table=event_name, contents_string='COUNT(*)', filter_string='id IS NOT NULL')
        return return_row[0][0]

    def record_donation(self, event_name, donation):
        self.create_event_table_if_not_exists(event_name=event_name)
        self.logger.log_info('Inserting donation: {} into donations database'.format(donation))
        self.db.insert_row(
            table=event_name,
            row_string='(NULL, ?, ?, ?)',
            row_data=(int(time.time()), donation.get_total_raised(), donation.get_donation_amount()))

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
        average_donation_row = self.db.get_specific_rows(
            table=event_name,
            contents_string='AVG(delta)',
            filter_string='id IS NOT NULL')
        return round(average_donation_row[0][0], 2)

    def get_event_names(self):
        names_to_remove = ('sqlite_sequence')
        return [name for name in self.db.get_table_names() if name not in names_to_remove]

    def get_donations_for_timespan(self, event_name, timespan_start, timespan_end=int(time.time())):
        donation_rows = self.db.get_specific_rows(table=event_name, filter_string='timestamp >= {} AND timestamp <= {}'.format(
            timespan_start,
            timespan_end))
        return [convert_row_to_donation(row) for row in donation_rows]

    def get_largest_donation(self, event_name):
        largest_donation_row = self.db.get_specific_rows(
            table=event_name,
            contents_string='id, timestamp, amount, MAX(delta)',
            filter_string='id IS NOT NULL')
        return convert_row_to_donation(largest_donation_row[0])
