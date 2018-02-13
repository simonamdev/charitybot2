import time

from pypika import Query, Order, Table, functions as fn

from charitybot2.models.donation import Donation
from charitybot2.paths import init_donations_script_path, init_events_script_path
from charitybot2.persistence.sql_script import SQLScript
from charitybot2.persistence.sqlite_repository import SQLiteRepository


class DonationAlreadyRegisteredException(Exception):
    pass


donations_table = Table('donations')


def fix_placeholders(query):
    return str(query).replace('\'', '')


class DonationSQLiteRepository(SQLiteRepository):
    def __init__(self, db_path='memory', debug=False):
        super().__init__(db_path=db_path, debug=debug)
        self.__validate_repository()

    def __validate_repository(self):
        donations_init_script = SQLScript(path=init_donations_script_path)
        self.execute_query(query=donations_init_script.return_sql(), commit=True)
        events_init_script = SQLScript(path=init_events_script_path)
        self.execute_query(query=events_init_script.return_sql(), commit=True)

    def donation_exists(self, donation_internal_reference):
        if donation_internal_reference is None:
            return False
        q = Query.from_(donations_table).where(
            donations_table.internalReference == '?'
        ).select(
            fn.Count(fn.Star())
        )
        data = (donation_internal_reference, )
        count = self.execute_query(query=fix_placeholders(q), data=data).fetchone()[0]
        return count >= 1

    def record_donation(self, donation):
        donation_query = 'INSERT INTO `donations` ' \
                         'VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?);'
        donation_data = (
            donation.amount,
            donation.event_identifier,
            donation.timestamp,
            donation.internal_reference,
            donation.external_reference,
            donation.donor_name,
            donation.notes,
            donation.validity)
        self.execute_query(query=donation_query, data=donation_data, commit=True)

    def get_event_donations(self, event_identifier, limit=None):
        q = Query.from_(donations_table).where(
            donations_table.eventInternalName == '?')\
            .select(fn.Star())\
            .orderby('timeRecorded', order=Order.desc)
        if limit is not None and isinstance(limit, int):
            q = q.limit(limit)
        data = (event_identifier, )
        rows = self.execute_query(query=fix_placeholders(q), data=data).fetchall()
        return [self.__convert_row_to_donation(row) for row in rows]

    def get_latest_event_donation(self, event_identifier):
        latest_donation = self.get_event_donations(event_identifier=event_identifier, limit=1)
        return latest_donation[0] if len(latest_donation) > 0 else None

    def get_time_filtered_event_donations(self, event_identifier, lower_bound=0, upper_bound=None, limit=None):
        query = 'SELECT * ' \
                'FROM `donations` ' \
                'WHERE eventInternalName = ? ' \
                'AND timeRecorded BETWEEN ? AND ? ' \
                'ORDER BY timeRecorded DESC'
        if limit is not None:
            query += ' LIMIT ?;'
            data = (event_identifier, lower_bound, upper_bound if upper_bound else time.time(), limit)
        else:
            query += ';'
            data = (event_identifier, lower_bound, upper_bound if upper_bound else time.time())
        rows = self.execute_query(query=query, data=data).fetchall()
        return [self.__convert_row_to_donation(row) for row in rows]

    def get_largest_donation(self, event_identifier):
        query = 'SELECT * ' \
                'FROM `donations` ' \
                'WHERE eventInternalName = ? ' \
                'ORDER BY amount DESC ' \
                'LIMIT 1;'
        data = (event_identifier, )
        row = self.execute_query(query=query, data=data).fetchone()
        return self.__convert_row_to_donation(row=row) if row is not None else None

    def get_donation_count(self, event_identifier, time_lower_bound=0, time_upper_bound=None):
        query = 'SELECT COUNT(*) ' \
                'FROM `donations` ' \
                'WHERE eventInternalName = ? ' \
                'AND timeRecorded BETWEEN ? AND ?;'
        data = (event_identifier, time_lower_bound, time_upper_bound if time_upper_bound else time.time())
        if time_lower_bound == 0 and time_upper_bound is None:
            query = 'SELECT COUNT(*) ' \
                    'FROM `donations` ' \
                    'WHERE eventInternalName = ?;'
            data = (event_identifier, )
        row = self.execute_query(query=query, data=data).fetchone()
        return int(row[0])

    def get_average_donation_amount(self, event_identifier):
        query = 'SELECT AVG(amount) ' \
                'FROM `donations` ' \
                'WHERE eventInternalName = ?;'
        data = (event_identifier, )
        row = self.execute_query(query=query, data=data).fetchone()
        return float(row[0]) if row[0] else 0.0

    def get_donation_distribution(self, event_identifier):
        distribution_bounds = ((0, 10), (10, 20), (20, 50), (50, 75), (75, 100), (100, 10000))
        donations = self.get_event_donations(event_identifier=event_identifier)
        distribution = [0, 0, 0, 0, 0, 0]
        for donation in donations:
            for bounds in distribution_bounds:
                if bounds[0] <= donation.amount < bounds[1]:
                    distribution[distribution_bounds.index(bounds)] += 1
                    break
        return distribution

    @staticmethod
    def __convert_row_to_donation(row):
        donation = Donation(
            amount=row[1],
            event_identifier=row[2],
            timestamp=row[3],
            internal_reference=row[4],
            external_reference=row[5],
            donor_name=row[6],
            notes=row[7],
            valid=row[8]
        )
        return donation
