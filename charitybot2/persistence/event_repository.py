from charitybot2.creators.event_configuration_creator import EventConfigurationCreator
from charitybot2.paths import production_repository_db_path
from charitybot2.persistence.sqlite_repository import SQLiteRepository
from tests.paths_for_tests import test_repository_db_path


class EventAlreadyRegisteredException(Exception):
    pass


class EventNotRegisteredException(Exception):
    pass


class EventRepository(SQLiteRepository):
    def __init__(self, debug=False):
        self._db_path = production_repository_db_path if not debug else test_repository_db_path
        super().__init__(db_path=self._db_path)
        self.open_connection()
        self.__validate_repository()

    @property
    def db_path(self):
        return self._db_path

    def __validate_repository(self):
        event_table_create_query = 'CREATE TABLE IF NOT EXISTS `events` (' \
                                   '`eventId`          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,' \
                                   '`identifier`       TEXT NOT NULL,' \
                                   '`title`            TEXT NOT NULL,' \
                                   '`startTime`        INTEGER NOT NULL,' \
                                   '`endTime`          INTEGER NOT NULL,' \
                                   '`currencyKey`      TEXT NOT NULL,' \
                                   '`startingAmount`   REAL,' \
                                   '`targetAmount`     INTEGER NOT NULL,' \
                                   '`sourceUrl`        TEXT NOT NULL,' \
                                   '`updateDelay`      INTEGER);'
        self.execute_query(query=event_table_create_query, commit=True)

    def event_already_registered(self, identifier):
        query = 'SELECT COUNT(*) FROM `events` WHERE identifier = ?'
        data = (identifier, )
        count = self.execute_query(query=query, data=data).fetchall()
        return count[0][0] >= 1

    def get_event_configuration(self, identifier):
        if not self.event_already_registered(identifier=identifier):
            raise EventNotRegisteredException('Event by {} is not registered yet'.format(identifier))
        retrieve_query = 'SELECT * FROM `events` WHERE identifier = ?'
        retrieve_data = (identifier, )
        row = self.execute_query(query=retrieve_query, data=retrieve_data).fetchall()[0]
        return self.__convert_row_to_event_configuration(row=row)

    def register_event(self, event_configuration):
        if self.event_already_registered(identifier=event_configuration.identifier):
            raise EventAlreadyRegisteredException('Event by {} is already registered'.format(event_configuration.identifier))
        register_query = 'INSERT INTO `events` VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?);'
        register_data = (
            event_configuration.identifier,
            event_configuration.title,
            event_configuration.start_time,
            event_configuration.end_time,
            event_configuration.currency.key,
            0,
            event_configuration.target_amount,
            event_configuration.source_url,
            event_configuration.update_delay)
        self.execute_query(query=register_query, data=register_data, commit=True)

    def update_event(self, new_event_configuration):
        if not self.event_already_registered(identifier=new_event_configuration.identifier):
            raise EventNotRegisteredException('Event by {} is not registered yet'.format(new_event_configuration.identifier))
        update_query = 'UPDATE `events` ' \
                       'SET ' \
                       'title = ?, ' \
                       'startTime = ?, ' \
                       'endTime = ?, ' \
                       'currencyKey = ?, ' \
                       'targetAmount = ?, ' \
                       'sourceUrl = ?, ' \
                       'updateDelay = ? ' \
                       'WHERE identifier = ?'
        update_data = (new_event_configuration.title,
                       new_event_configuration.start_time,
                       new_event_configuration.end_time,
                       new_event_configuration.currency.key,
                       new_event_configuration.target_amount,
                       new_event_configuration.source_url,
                       new_event_configuration.update_delay,
                       new_event_configuration.identifier)
        self.execute_query(query=update_query, data=update_data, commit=True)

    @staticmethod
    def __convert_row_to_event_configuration(row):
        configuration_values = {
            'identifier': row[1],
            'title': row[2],
            'start_time': row[3],
            'end_time': row[4],
            'currency_key': row[5],
            'target_amount': row[7],
            'source_url': row[8],
            'update_delay': row[9]
        }
        return EventConfigurationCreator(configuration_values=configuration_values).configuration
