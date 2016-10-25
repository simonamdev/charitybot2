import os

from charitybot2.storage.donations_db import DonationsDB
from charitybot2.storage.events_db import EventsDB


class DBCouldNotBeFoundException(Exception):
    pass


class DBHandler:
    def __init__(self, events_db_path, donations_db_path, debug=False):
        self.events_db_path = events_db_path
        self.donations_db_path = donations_db_path
        self.debug = debug
        self.events_db = None
        self.donations_db = None
        self.validate_database_files()
        self.initialise_connections()

    def validate_database_files(self):
        if not os.path.isfile(self.events_db_path) or not os.path.isfile(self.donations_db_path):
            raise DBCouldNotBeFoundException

    def initialise_connections(self):
        self.events_db = EventsDB(db_path=self.events_db_path, debug=self.debug)
        self.donations_db = DonationsDB(db_path=self.donations_db_path, debug=self.debug)

    def get_events_db(self):
        return self.events_db

    def get_donations_db(self):
        return self.donations_db
