from charitybot2.models.donation import Donation
from charitybot2.paths import init_donations_script_path
from charitybot2.persistence.sql_script import SQLScript
from charitybot2.persistence.sqlite_repository import SQLiteRepository


class DonationAlreadyRegisteredException(Exception):
    pass


class DonationSQLiteRepository(SQLiteRepository):
    def __init__(self, db_path='memory', debug=False):
        super().__init__(db_path=db_path, debug=debug)
        self.__validate_repository()

    def __validate_repository(self):
        init_script = SQLScript(path=init_donations_script_path)
        self.execute_query(query=init_script.return_sql(), commit=True)

    def __donation_already_stored(self, identifier):
        if identifier is None:
            return False
        query = 'SELECT COUNT(*) ' \
                'FROM `donations` ' \
                'WHERE identifier = ?;'
        data = (identifier, )
        count = self.execute_query(query=query, data=data).fetchone()[0]
        return count >= 1

    def record_donation(self, donation):
        if self.__donation_already_stored(identifier=donation.identifier):
            raise DonationAlreadyRegisteredException(
                'Donation with identifier: {} is already registered'.format(donation.identifier))
        query = 'INSERT INTO `donations` ' \
                'VALUES (NULL, ?, ?, ?, ?, ?, ?);'
        data = (
            donation.amount,
            donation.event_identifier,
            donation.timestamp,
            donation.identifier,
            donation.notes,
            donation.validity)
        self.execute_query(query=query, data=data, commit=True)

    def get_event_donations(self, event_identifier):
        # TODO: Add event identifier validation here
        query = 'SELECT * ' \
                'FROM `donations` ' \
                'WHERE eventInternalName = ?;'
        data = (event_identifier, )
        rows = self.execute_query(query=query, data=data).fetchall()
        return [self.__convert_row_to_donation(row) for row in rows]

    def get_latest_event_donation(self, event_identifier):
        query = 'SELECT * ' \
                'FROM `donations` ' \
                'WHERE eventInternalName = ? ' \
                'ORDER BY timeRecorded DESC ' \
                'LIMIT 1;'
        data = (event_identifier, )
        row = self.execute_query(query=query, data=data).fetchall()[0]
        return self.__convert_row_to_donation(row=row)

    def get_time_filtered_event_donations(self, event_identifier, lower_bound, upper_bound=None):
        query = 'SELECT * ' \
                'FROM `donations` ' \
                'WHERE eventInternalName = ? ' \
                'AND timeRecorded BETWEEN ? AND ? ' \
                'ORDER BY timeRecorded DESC;'
        data = (event_identifier, lower_bound, upper_bound)
        rows = self.execute_query(query=query, data=data).fetchall()
        return [self.__convert_row_to_donation(row) for row in rows]

    @staticmethod
    def __convert_row_to_donation(row):
        donation = Donation(
            amount=row[1],
            event_identifier=row[2],
            timestamp=row[3],
            identifier=row[4],
            notes=row[5],
            valid=row[6]
        )
        return donation
