from charitybot2.models.log import Log
from charitybot2.paths import production_logs_db_path
from charitybot2.persistence.console_logger import ConsoleLogger
from charitybot2.persistence.logger import Logger
from charitybot2.persistence.sqlite_repository import SQLiteRepository


class RepositoryLogger(Logger):
    def __init__(self, source, event, debug=False):
        self._source = source
        self._event = event
        self._debug = debug
        self._console_logger = ConsoleLogger(source=source, event=event)
        db_path = production_logs_db_path if not self._debug else ':memory:'
        self._repository = SQLiteRepository(db_path=db_path)
        self._repository.open_connection()
        self.__validate_logs_repository()
        super().__init__(source=source, event=event)

    def log(self, log):
        self._console_logger.log(log=log)
        self.__store_log_in_repository(log=log)

    def __store_log_in_repository(self, log):
        log_storage_query = 'INSERT INTO `logs` VALUES (NULL, ?, ?, ?, ?, ?)'
        query_data = (log.timestamp, log.level, log.source, log.event, log.message)
        self._repository.execute_query(query=log_storage_query, data=query_data, commit=True)

    def __validate_logs_repository(self):
        table_create_query = 'CREATE TABLE IF NOT EXISTS `logs` (' \
                             '`id`	      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,' \
                             '`timestamp` INTEGER NOT NULL,' \
                             '`level`	  INTEGER NOT NULL DEFAULT 0,' \
                             '`source`    TEXT NOT NULL,' \
                             '`event`	  TEXT NOT NULL,' \
                             '`message`   TEXT NOT NULL' \
                             ');'
        self._repository.execute_query(query=table_create_query, commit=True)

    @staticmethod
    def __convert_row_to_log(row):
        return Log(timestamp=row[1], level=row[2], source=row[3], event=row[4], message=row[5])

    def get_all_logs(self):
        all_logs_query = 'SELECT * FROM `logs`'
        logs = self._repository.execute_query(query=all_logs_query).fetchall()
        return [self.__convert_row_to_log(row=row) for row in logs]

    def get_specific_logs(self, timestamp=None, level=None, source=None, event=None):
        if all(param is None for param in (timestamp, level, source, event)):
            return self.get_all_logs()
        filter_query = 'SELECT * from `logs` WHERE'
        filter_data = []
        filters_applied = 0
        if timestamp is not None:
            if isinstance(timestamp, int) or isinstance(timestamp, float):
                filter_query += ' timestamp <= ?'
                filter_data.append(timestamp)
            elif isinstance(timestamp, tuple) or isinstance(timestamp, list):
                if len(timestamp) > 2:
                    timestamp = (timestamp[0], timestamp[1])
                if len(timestamp) == 2 and timestamp[0] > timestamp[1]:
                    timestamp = list(timestamp)
                    timestamp.reverse()
                filter_query += ' timestamp >= ? AND timestamp <= ?'
                filter_data.extend(timestamp)
            filters_applied += 1
        if level is not None:
            if filters_applied > 1:
                filter_query += ' AND '
            filter_query += ' level = ?'
            filter_data.append(level)
            filters_applied += 1
        if source is not None:
            if filters_applied > 1:
                filter_query += ' AND '
            filter_query += ' source = ?'
            filter_data.append(source)
            filters_applied += 1
        if event is not None:
            if filters_applied > 1:
                filter_query += ' AND'
            filter_query += ' event = ?'
            filter_data.append(event)
        filtered_logs = self._repository.execute_query(query=filter_query, data=tuple(filter_data)).fetchall()
        return [self.__convert_row_to_log(row=row) for row in filtered_logs]
