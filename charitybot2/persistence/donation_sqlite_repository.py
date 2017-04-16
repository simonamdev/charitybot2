from charitybot2.persistence.sqlite_repository import SQLiteRepository


class DonationAlreadyRegisteredException(Exception):
    pass


class DonationSQLiteRepository(SQLiteRepository):
    def __init__(self, db_path='memory', debug=False):
        super().__init__(db_path=db_path, debug=debug)

    def record_donation(self, donation):
        pass

    def get_event_donations(self, event_identifier):
        pass

    def get_latest_event_donation(self, event_identifier):
        pass
