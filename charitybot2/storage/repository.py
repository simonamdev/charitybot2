import time
import sqlite3

from charitybot2.botconfig.event_config import EventConfigurationCreator
from charitybot2.events.donation import Donation
from charitybot2.storage.logger import Logger


class EventNotRegisteredException(Exception):
    pass


def convert_donation_row_to_object(row):
    return Donation(old_amount=(row[4] - row[3]), new_amount=row[4], timestamp=row[2], notes=row[5], valid=row[6])


def convert_event_row_to_configuration(row):
    config_data = {
        'internal_name': row[1],
        'external_name': row[2],
        'start_time': row[3],
        'end_time': row[4],
        'currency_key': row[5],
        'target_amount': int(row[7]),
        'source_url': row[8],
        'update_delay': row[9]
    }
    return EventConfigurationCreator(config_values=config_data).get_event_configuration()


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
        query = 'SELECT COUNT(*) ' \
                'FROM `events`' \
                'WHERE internalName = (?)'
        data = (event_name, )
        event_count = self.connection.execute(query, data).fetchone()[0]
        return 1 == event_count

    def register_event(self, event_configuration):
        query = 'INSERT INTO `events`' \
                '(eventId, internalName, externalName, startTime, endTime, currencyId, startingAmount, targetAmount, sourceUrl, updateDelay)' \
                'VALUES' \
                '(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?);'
        data = (
            event_configuration.get_value('internal_name'),
            event_configuration.get_value('external_name'),
            event_configuration.get_value('start_time'),
            event_configuration.get_value('end_time'),
            event_configuration.get_value('currency_key'),
            0,
            event_configuration.get_value('target_amount'),
            event_configuration.get_value('source_url'),
            event_configuration.get_value('update_delay'))
        self.cursor.execute(query, data)
        self.connection.commit()

    def update_event(self, event_configuration):
        query = 'UPDATE `events`' \
                'SET ' \
                'externalName = (?),' \
                'startTime = (?),' \
                'endTime = (?),' \
                'currencyId = (?),' \
                'targetAmount = (?),' \
                'sourceUrl = (?),' \
                'updateDelay = (?)' \
                'WHERE eventId = (?)'
        data = (
            event_configuration.get_value('external_name'),
            event_configuration.get_value('start_time'),
            event_configuration.get_value('end_time'),
            event_configuration.get_value('currency_key'),
            event_configuration.get_value('target_amount'),
            event_configuration.get_value('source_url'),
            event_configuration.get_value('update_delay'),
            self.get_event_id(event_configuration.get_value('internal_name')))
        self.cursor.execute(query, data)
        self.connection.commit()

    def get_event_configuration(self, event_name):
        query = 'SELECT *' \
                'FROM `events`' \
                'WHERE eventId = (?)'
        data = (self.get_event_id(event_name), )
        event_row = self.cursor.execute(query, data).fetchone()
        return convert_event_row_to_configuration(event_row)

    def get_number_of_donations(self, event_name):
        query = 'SELECT COUNT(*)' \
                'FROM `donations`' \
                'WHERE eventId = (?)'
        data = (self.get_event_id(event_name), )
        return self.cursor.execute(query, data).fetchone()[0]

    def donations_are_present(self, event_name):
        return self.get_number_of_donations(event_name=event_name) > 0

    def get_all_donations(self, event_name):
        query = 'SELECT *' \
                'FROM `donations`' \
                'WHERE eventId = (?)'
        data = (self.get_event_id(event_name), )
        return [convert_donation_row_to_object(row) for row in self.cursor.execute(query, data).fetchall()]

    def record_donation(self, event_name, donation):
        self.logger.log_verbose('Inserting donation: {} into donations database'.format(donation))
        query = 'INSERT INTO `donations` ' \
                '(donationId, eventId, timeRecorded, donationAmount, runningTotal, notes, valid)' \
                'VALUES' \
                '(NULL, ?, ?, ?, ?, ?, ?)'
        data = (
            self.get_event_id(event_name),
            donation.get_timestamp(),
            donation.get_donation_amount(),
            donation.get_total_raised(),
            donation.get_notes(),
            1 if donation.get_validity() else 0)
        self.cursor.execute(query, data)
        self.connection.commit()

    def get_last_donation(self, event_name, get_invalid=False):
        if self.get_number_of_donations(event_name=event_name) == 0:
            return self.get_starting_amount(event_name=event_name)
        valid_where_query = 'AND valid = 1 ' if not get_invalid else ''
        query = 'SELECT *' \
                'FROM `donations`' \
                'WHERE eventId = (?) {}' \
                'ORDER BY timeRecorded DESC ' \
                'LIMIT 1'.format(valid_where_query)
        data = (self.get_event_id(event_name), )
        last_donation_row = self.cursor.execute(query, data).fetchone()
        return convert_donation_row_to_object(last_donation_row)

    def get_total_raised(self, event_name):
        last_donation = self.get_last_donation(event_name=event_name, get_invalid=True)
        return last_donation.get_total_raised() if isinstance(last_donation, Donation) else last_donation

    def get_average_donation(self, event_name):
        if self.get_number_of_donations(event_name=event_name) == 0:
            return 0.0
        query = 'SELECT AVG(donationAmount)' \
                'FROM `donations`' \
                'WHERE eventId = (?) AND valid = 1'
        data = (self.get_event_id(event_name=event_name), )
        average = self.cursor.execute(query, data).fetchone()[0]
        return round(average, 2)

    def get_event_names(self):
        query = 'SELECT internalName ' \
                'FROM `events`'
        names = self.cursor.execute(query).fetchall()
        return [name[0] for name in names]

    def get_donations_for_timespan(self, event_name, timespan_start, timespan_end=int(time.time())):
        query = 'SELECT * ' \
                'FROM `donations`' \
                'WHERE eventId = (?) AND timeRecorded BETWEEN (?) AND (?) AND valid = 1'
        data = (self.get_event_id(event_name), timespan_start, timespan_end)
        return [convert_donation_row_to_object(row) for row in self.cursor.execute(query, data).fetchall()]

    def get_largest_donation(self, event_name):
        if self.get_number_of_donations(event_name=event_name) == 0:
            return None
        query = 'SELECT *' \
                'FROM `donations`' \
                'WHERE eventId = (?)' \
                'ORDER BY donationAmount DESC, timeRecorded DESC ' \
                'LIMIT 1'
        data = (self.get_event_id(event_name), )
        largest_donation = self.cursor.execute(query, data).fetchone()
        return convert_donation_row_to_object(largest_donation)

    def get_starting_amount(self, event_name):
        query = 'SELECT startingAmount ' \
                'FROM `events` ' \
                'WHERE eventId = (?)'
        data = (self.get_event_id(event_name), )
        return self.cursor.execute(query, data).fetchone()[0]

