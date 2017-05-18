from charitybot2.creators.event_configuration_creator import EventConfigurationCreator
from charitybot2.paths import init_events_script_path
from charitybot2.persistence.sql_script import SQLScript
from charitybot2.persistence.sqlite_repository import SQLiteRepository


class EventAlreadyRegisteredException(Exception):
    pass


class EventNotRegisteredException(Exception):
    pass


class EventSQLiteRepository(SQLiteRepository):
    def __init__(self, db_path='memory', debug=False):
        super().__init__(db_path=db_path, debug=debug)
        self.__validate_repository()

    @property
    def db_path(self):
        return self._db_path

    def __validate_repository(self):
        init_script = SQLScript(path=init_events_script_path)
        self.execute_query(query=init_script.return_sql(), commit=True)

    def event_already_registered(self, identifier):
        query = 'SELECT COUNT(*) FROM `events` WHERE internalName = ?'
        data = (identifier, )
        count = self.execute_query(query=query, data=data).fetchall()
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
        register_query = 'INSERT INTO `events` VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'
        register_data = (
            event_configuration.identifier,
            event_configuration.title,
            event_configuration.start_time,
            event_configuration.end_time,
            event_configuration.currency.key,
            0.0,
            0.0,
            event_configuration.target_amount,
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

    # TODO: Deprecate this method, move it to a transaction in the donation repository
    def update_event_current_amount(self, identifier, current_amount):
        if not self.event_already_registered(identifier=identifier):
            raise EventNotRegisteredException('Event by {} is not registered yet'.format(identifier))
        update_query = 'UPDATE `events` ' \
                       'SET currentAmount = ? ' \
                       'WHERE internalName = ?'
        update_data = (current_amount, identifier)
        self.execute_query(query=update_query, data=update_data, commit=True)

    @staticmethod
    def __convert_row_to_event_configuration(row):
        configuration_values = {
            'identifier': row[0],
            'title': row[1],
            'start_time': row[2],
            'end_time': row[3],
            'currency_key': row[4],
            'target_amount': row[7],
            'source_url': row[8],
            'update_delay': row[9]
        }
        return EventConfigurationCreator(configuration_values=configuration_values).configuration
