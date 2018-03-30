import time
from pypika import Query, Table, functions as fn

from charitybot2.creators.event_configuration_creator import EventConfigurationCreator
from charitybot2.paths import init_events_script_path
from charitybot2.persistence.sql_script import SQLScript
from charitybot2.persistence.sqlite_repository import SQLiteRepository


class EventAlreadyRegisteredException(Exception):
    pass


class EventNotRegisteredException(Exception):
    pass


class EventInvalidValueException(Exception):
    pass


events_table = Table('events')


def fix_placeholders(query):
    return str(query).replace('\'', '')


class EventSQLiteRepository(SQLiteRepository):
    def __init__(self, db_path='memory', debug=False):
        super().__init__(db_path=db_path, debug=debug)
        self.__validate_repository()

    def __validate_repository(self):
        init_script = SQLScript(path=init_events_script_path)
        self.execute_query(query=init_script.return_sql(), commit=True)

    def get_all_identifiers(self):
        q = Query.from_(events_table)\
            .select('internalName')
        rows = self.execute_query(query=fix_placeholders(q)).fetchall()
        return [row[0] for row in rows]

    def event_already_registered(self, identifier):
        q = Query.from_(events_table).where(
            events_table.internalName == '?'
        ).select(
            fn.Count(fn.Star())
        )
        data = (identifier, )
        count = self.execute_query(query=fix_placeholders(q), data=data).fetchall()
        return count[0][0] >= 1

    def get_event_configuration(self, identifier):
        if not self.event_already_registered(identifier=identifier):
            raise EventNotRegisteredException('Event by {} is not registered yet'.format(identifier))
        retrieve_query = 'SELECT * ' \
                         'FROM `events` ' \
                         'WHERE internalName = ?'
        retrieve_data = (identifier, )
        row = self.execute_query(query=retrieve_query, data=retrieve_data).fetchall()[0]
        return self.__convert_row_to_event_configuration(row=row)

    def register_event(self, event_configuration):
        if self.event_already_registered(identifier=event_configuration.identifier):
            raise EventAlreadyRegisteredException('Event by {} is already registered'.format(event_configuration.identifier))
        register_query = 'INSERT INTO `events` VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'
        register_data = (
            event_configuration.identifier,
            event_configuration.title,
            event_configuration.start_time,
            event_configuration.end_time,
            event_configuration.currency.key,
            0.0,
            0.0,
            event_configuration.target_amount,
            event_configuration.source,
            event_configuration.source_url,
            event_configuration.update_delay)
        self.execute_query(query=register_query, data=register_data, commit=True)

    def update_event(self, new_event_configuration):
        if not self.event_already_registered(identifier=new_event_configuration.identifier):
            raise EventNotRegisteredException('Event by {} is not registered yet'.format(new_event_configuration.identifier))
        update_query = 'UPDATE `events` ' \
                       'SET ' \
                       'externalName = ?, ' \
                       'startTime = ?, ' \
                       'endTime = ?, ' \
                       'currencyKey = ?, ' \
                       'targetAmount = ?, ' \
                       'sourceUrl = ?, ' \
                       'updateDelay = ? ' \
                       'WHERE internalName = ?'
        update_data = (new_event_configuration.title,
                       new_event_configuration.start_time,
                       new_event_configuration.end_time,
                       new_event_configuration.currency.key,
                       new_event_configuration.target_amount,
                       new_event_configuration.source_url,
                       new_event_configuration.update_delay,
                       new_event_configuration.identifier)
        self.execute_query(query=update_query, data=update_data, commit=True)

    def get_event_starting_amount(self, identifier):
        if not self.event_already_registered(identifier=identifier):
            raise EventNotRegisteredException('Event by {} is not registered yet'.format(identifier))
        retrieve_query = 'SELECT startingAmount ' \
                         'FROM `events` ' \
                         'WHERE internalName = ?'
        retrieve_data = (identifier, )
        return self.execute_query(query=retrieve_query, data=retrieve_data).fetchall()[0][0]

    def update_event_starting_amount(self, identifier, start_amount):
        if not self.event_already_registered(identifier=identifier):
            raise EventNotRegisteredException('Event by {} is not registered yet'.format(identifier))
        update_query = 'UPDATE `events` ' \
                       'SET startingAmount = ? ' \
                       'WHERE internalName = ?'
        update_data = (start_amount, identifier)
        self.execute_query(query=update_query, data=update_data, commit=True)

    def get_event_current_amount(self, identifier):
        if not self.event_already_registered(identifier=identifier):
            raise EventNotRegisteredException('Event by {} is not registered yet'.format(identifier))
        retrieve_query = 'SELECT currentAmount ' \
                         'FROM `events` ' \
                         'WHERE internalName = ?'
        retrieve_data = (identifier, )
        return self.execute_query(query=retrieve_query, data=retrieve_data).fetchall()[0][0]

    def update_event_current_amount(self, identifier, current_amount):
        if not self.event_already_registered(identifier=identifier):
            raise EventNotRegisteredException('Event by {} is not registered yet'.format(identifier))
        if not (isinstance(current_amount, float) or isinstance(current_amount, int)):
            raise TypeError('Event Total must be float or int, not {}'.format(type(current_amount)))
        update_query = 'UPDATE `events` ' \
                       'SET currentAmount = ? ' \
                       'WHERE internalName = ?'
        update_data = (current_amount, identifier)
        self.execute_query(query=update_query, data=update_data, commit=True)

    def update_event_target_amount(self, identifier, target_amount):
        if not self.event_already_registered(identifier=identifier):
            raise EventNotRegisteredException('Event by {} is not registered yet'.format(identifier))
        update_query = 'UPDATE `events` ' \
                       'SET targetAmount = ? ' \
                       'WHERE internalName = ?'
        update_data = (target_amount, identifier)
        self.execute_query(query=update_query, data=update_data, commit=True)

    def get_events(self):
        query = 'SELECT * FROM `events`;'
        events = self.execute_query(query=query).fetchall()
        return [self.__convert_row_to_event_configuration(row=row) for row in events]

    def get_ongoing_events(self, current_time, buffer_in_minutes=15):
        # Convert the buffer to seconds
        buffer_in_seconds = buffer_in_minutes * 60
        q = Query.from_(events_table) \
            .select(
                'internalName',
                'title',
                'startTime',
                'endTime'
            ).where(
                (events_table.startTime - buffer_in_seconds) <= current_time
            ).where(
                (events_table.endTime + buffer_in_seconds) >= current_time
            )
        rows = self.execute_query(query=fix_placeholders(q)).fetchall()
        return [
            {
                'identifier': row[0],
                'title': row[1],
                'start_time': row[2],
                'end_time': row[3]
            } for row in rows
        ]

    def get_upcoming_events(self, current_time=None, hours_in_advance=24):
        current_time = int(time.time()) if current_time is None else current_time
        advance_in_seconds = hours_in_advance * 60 * 60
        q = Query.from_(events_table) \
            .select(
            'internalName',
            'title',
            'startTime',
            'endTime'
        ).where(
            events_table.startTime > current_time
        ).where(
            events_table.endTime <= (current_time + advance_in_seconds)
        )
        rows = self.execute_query(query=fix_placeholders(q)).fetchall()
        return [
            {
                'identifier': row[0],
                'title': row[1],
                'start_time': row[2],
                'end_time': row[3]
            } for row in rows
        ]

    @staticmethod
    def __convert_row_to_event_configuration(row):
        configuration_values = {
            'identifier': row[0],
            'title': row[1],
            'start_time': row[2],
            'end_time': row[3],
            'currency_key': row[4],
            'target_amount': row[7],
            'source_details': {
                'source': row[8],
                'url': row[9]
            },
            'update_delay': row[10]
        }
        return EventConfigurationCreator(configuration_values=configuration_values).configuration
