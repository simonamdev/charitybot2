from neopysqlite.neopysqlite import Neopysqlite
from neopysqlite.neopysqlite import exception as npysql

events_db_file_name = 'events.db'


class EventsDB:
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
        print(self.db.get_all_rows(table='events'))
        event_names = [row[1] for row in self.db.get_all_rows(table='events')]
        return event_name in event_names
