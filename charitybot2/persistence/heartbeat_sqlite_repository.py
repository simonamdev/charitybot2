import time
from charitybot2.persistence.sqlite_repository import SQLiteRepository


class NonExistentHeartbeatSource(Exception):
    pass


class HeartbeatSQLiteRepository(SQLiteRepository):
    def __init__(self, db_path='memory', debug=False):
        super().__init__(db_path=db_path, debug=debug)
        self.__validate_repository()

    def __validate_repository(self):
        heartbeat_table_create_query = 'CREATE TABLE IF NOT EXISTS `heartbeats` (' \
                                       '`entryId`       INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,' \
                                       '`source`        TEXT NOT NULL,' \
                                       '`state`         TEXT NOT NULL,' \
                                       '`timestamp`     INTEGER NOT NULL' \
                                       ');'
        self.execute_query(query=heartbeat_table_create_query, commit=True)

    def __validate_source_exists(self, source):
        pass

    def store_heartbeat(self, source, state, timestamp=None):
        heartbeat_insert_query = 'INSERT INTO `heartbeats` ' \
                                 '(source, state, timestamp) ' \
                                 'VALUES ' \
                                 '(?, ?, ?);'
        if timestamp is None:
            timestamp = int(time.time())
        heartbeat_insert_data = (source, state, timestamp)
        self.execute_query(query=heartbeat_insert_query, data=heartbeat_insert_data, commit=True)

    def get_last_heartbeat(self, source):
        heartbeat_retrieve_last_query = 'SELECT * ' \
                                        'FROM `heartbeats` ' \
                                        'WHERE source = ? ' \
                                        'ORDER BY timestamp ' \
                                        'LIMIT 1;'
        heartbeat_retrieve_last_data = (source, )
        return_data = self.execute_query(query=heartbeat_retrieve_last_query, data=heartbeat_retrieve_last_data)
        fetched_data = return_data.fetchall()
        if len(fetched_data) == 0:
            raise NonExistentHeartbeatSource('No Heartbeats available by that source')
        return_data = fetched_data[0]
        return {
            'source': return_data[1],
            'state': return_data[2],
            'timestamp': return_data[3]
        }
