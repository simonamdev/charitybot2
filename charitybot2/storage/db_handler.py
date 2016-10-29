import os

from charitybot2.storage.donations_db import DonationsDB


class DBCouldNotBeFoundException(Exception):
    pass


class DBHandler:
    def __init__(self, donations_db_path, debug=False):
        self.donations_db_path = donations_db_path
        self.debug = debug
        self.donations_db = None
        self.validate_database_files()
        self.initialise_connections()

    def validate_database_files(self):
        if not os.path.isfile(self.donations_db_path):
            raise DBCouldNotBeFoundException

    def initialise_connections(self):
        self.donations_db = DonationsDB(db_path=self.donations_db_path, debug=self.debug)

    def get_donations_db(self):
        return self.donations_db
