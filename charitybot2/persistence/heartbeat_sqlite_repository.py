from charitybot2.persistence.sqlite_repository import SQLiteRepository


class HeartbeatSQLiteRepository(SQLiteRepository):
    def store_state(self, state, timestamp=None):
        pass
