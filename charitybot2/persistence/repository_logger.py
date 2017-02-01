from charitybot2.models.log import Log
from charitybot2.paths import production_logs_db_path
from charitybot2.persistence.console_logger import ConsoleLogger
from charitybot2.persistence.logger import Logger
from charitybot2.persistence.sqlite_repository import SQLiteRepository


class RepositoryLogger(Logger):
    def __init__(self, source, event):
        self._source = source
        self._event = event
        self._console_logger = ConsoleLogger(source=source, event=event)
        self._repository = SQLiteRepository(db_path=production_logs_db_path)
        self.__validate_logs_repository()
        super().__init__(source=source, event=event)

    def log(self, log):
        self._console_logger.log(log=log)
        self.__store_log_in_repository(log=log)

    def __store_log_in_repository(self, log):
        self._repository.open_connection()
        log_storage_query = 'INSERT INTO `logs` VALUES (NULL, ?, ?, ?, ?, ?)'
        query_data = (log.timestamp, log.level, log.source, log.event, log.message)
        self._repository.execute_query(query=log_storage_query, data=query_data, commit=True)
        self._repository.close_connection()

    def __validate_logs_repository(self):
        self._repository.open_connection()
        table_create_query = 'CREATE TABLE IF NOT EXISTS `logs` (' \
                             '`id`	    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,' \
                             '`time`	INTEGER NOT NULL,' \
                             '`level`	INTEGER NOT NULL DEFAULT 0,' \
                             '`source`  TEXT NOT NULL,' \
                             '`event`	TEXT NOT NULL,' \
                             '`message` TEXT NOT NULL' \
                             ');'
        self._repository.execute_query(query=table_create_query, commit=True)
        self._repository.close_connection()

    @staticmethod
    def __convert_row_to_log(row):
        return Log(timestamp=row[1], level=row[2], source=row[3], event=row[4], message=row[5])

    def get_all_logs(self):
        self._repository.open_connection()
        all_logs_query = 'SELECT * FROM `logs`'
        logs = self._repository.execute_query(query=all_logs_query).fetchall()
        self._repository.close_connection()
        return [self.__convert_row_to_log(row=row) for row in logs]

    def get_specific_logs(self, timestamp=None, level=None, source=None, event=None):
        if all(param is None for param in (timestamp, level, source, event)):
            return self.get_all_logs()
