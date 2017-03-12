from charitybot2.persistence.sqlite_repository import SQLiteRepository


class NonExistentHeartbeat(Exception):
    pass


class HeartbeatSQLiteRepository(SQLiteRepository):
    def __init__(self, db_path='', debug=False):
        super().__init__(db_path=db_path, debug=debug)
        self.open_connection()
        self.__validate_repository()

    def __validate_repository(self):
        heartbeat_table_create_query = 'CREATE TABLE IF NOT EXISTS `heartbeats` (' \
                                       '`entryId`       INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,' \
                                       '`source`        TEXT NOT NULL,' \
                                       '`state`         TEXT NOT NULL,' \
                                       '`timestamp`     INTEGER NOT NULL' \
                                       ');'
        self.execute_query(query=heartbeat_table_create_query, commit=True)

    def store_heartbeat(self, source, state, timestamp=None):
        pass

    def get_last_heartbeat(self, source):
        pass
