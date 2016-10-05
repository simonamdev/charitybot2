import uuid
from neopysqlite.neopysqlite import Neopysqlite
from neopysqlite.neopysqlite import exception as npysql


events_db_file_name = 'events.db'


class EventAlreadyRegisteredException(Exception):
    pass


class EventsDB:
    event_default_state = 'REGISTERED'
    event_possible_states = [
        'REGISTERED',
        'ONGOING',
        'COMPLETED'
    ]

    def __init__(self, db_path=events_db_file_name, verbose=False):
        self.db_path = db_path
        self.verbose = verbose
        self.db = None
        self.initialise_db()

    def print(self, print_string):
        if self.verbose:
            print('[EDB] ' + print_string)

    def initialise_db(self):
        try:
            self.db = Neopysqlite(database_name='Events DB', db_path=self.db_path, verbose=self.verbose)
        except npysql.PysqliteCannotAccessException:
            self.print('Events DB does not exist, creating now')
            self.create_db()

    def create_db(self):
        open(self.db_path, 'w')
        self.print('Created DB at path: {}'.format(self.db_path))

    def event_exists(self, event_name):
        return event_name in self.get_all_event_names()

    def get_all_event_names(self):
        return [row[1] for row in self.db.get_all_rows(table='events')]

    def get_event_metadata(self, event_name):
        row = self.db.get_specific_rows(table='events', filter_string='name = \'{}\''.format(event_name))[0]
        return {
            'name': row[1],
            'uuid': row[2],
            'state': row[3]
        }

    def register_event(self, event_name):
        if event_name in self.get_all_event_names():
            raise EventAlreadyRegisteredException('Event with name: {} is already registered'.format(event_name))
        event_uuid = uuid.uuid4().bytes
        self.db.insert_row(table='events', row_string='(NULL, ?, ?, ?)', row_data=(event_name, event_uuid, EventsDB.event_default_state))

    def change_event_state(self, event_name, new_state):
        self.db.update_rows(table='events', update_string='state = ?', update_values=(new_state,), filter_string='name = \'{}\''.format(event_name))
