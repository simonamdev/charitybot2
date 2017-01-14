import time
import sqlite3

from charitybot2.events.donation import Donation
from charitybot2.storage.logger import Logger


class EventNotRegisteredException(Exception):
    pass


def convert_row_to_donation(row):
    return Donation(old_amount=(row[4] - row[3]), new_amount=row[4], timestamp=row[2], notes=row[5], valid=row[6])


class Repository:
    def __init__(self, db_path, debug=False):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.debug = debug
        self.logger = Logger(source='Donations_DB',  event='', console_only=debug)

    def get_event_id(self, event_name):
        query = 'SELECT `eventId`' \
                'FROM `events`' \
                'WHERE events.internalName = (?)'
        data = (event_name, )
        event_id = self.connection.execute(query, data).fetchone()
        if event_id is None:
            raise EventNotRegisteredException('Event: {} is not registered yet')
        return event_id[0]

    def event_exists(self, event_name):
        query = 'SELECT COUNT(*)' \
                'FROM `events`' \
                'WHERE internalName = (?)'
        data = (event_name, )
        return 1 == self.connection.execute(query, data).fetchone()[0]

    def register_event(self, event_configuration):
        query = 'INSERT INTO `events`' \
                '(eventId, internalName, externalName, startTime, endTime, currencyId, startingAmount, sourceUrl, updateDelay)' \
                'VALUES' \
                '(NULL, ?, ?, ?, ?, ?, ?, ?, ?);'
        data = (internal_name, external_name,)
        self.cursor.execute(query, data)

    def get_number_of_donations(self, event_name):
        query = 'SELECT COUNT(*)' \
                'FROM `donations`' \
                'WHERE eventId = (?)'
        data = (self.get_event_id(event_name), )
        return self.connection.execute(query, data).fetchone()[0]

    def get_all_donations(self, event_name):
        query = 'SELECT *' \
                'FROM `donations`' \
                'WHERE eventId = (?)'
        data = (self.get_event_id(event_name), )
        return [convert_row_to_donation(row) for row in self.connection.execute(query, data).fetchall()]

    def record_donation(self, event_name, donation):
        self.logger.log_verbose('Inserting donation: {} into donations database'.format(donation))
        query = 'INSERT INTO `donations` ' \
                '(donationId, eventId, timeRecorded, donationAmount, runningTotal, notes, valid)' \
                'VALUES' \
                '(NULL, ?, ?, ?, ?, ?, ?)'
        data = (
            self.get_event_id(event_name),
            int(time.time()),
            donation.get_donation_amount(),
            donation.get_total_raised(),
            donation.get_notes(),
            1 if donation.get_validity() else 0)
        self.connection.execute(query, data)

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
