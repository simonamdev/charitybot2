import time

from charitybot2.storage.base_db import BaseDB


class LogSourceDoesNotExistException(Exception):
    pass


class Log:
    info_level = 0
    warning_level = 1
    error_level = 2

    def __init__(self, source, timestamp, level, message):
        self.source = source
        self.timestamp = timestamp
        self.level = level
        self.message = message

    def __str__(self):
        return '[{}] [{}] [{}] [{}]'.format(
            self.timestamp,
            self.level,
            self.source,
            self.message
        )

    def get_time(self):
        return self.timestamp

    def get_message(self):
        return self.message

    def get_level(self):
        return self.level


class LogsDB(BaseDB):
    log_table_create_statement = 'CREATE TABLE IF NOT EXISTS `{}` (' \
                                 '`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,' \
                                 '`time`	INTEGER NOT NULL,' \
                                 '`level`	INTEGER NOT NULL DEFAULT 0,' \
                                 '`message`	TEXT NOT NULL' \
                                 ');  '

    def __init__(self, db_path, verbose=False):
        super().__init__(file_path=db_path, db_name='Logs DB', verbose=verbose)
        self.initialise()

    def create_log_source_table(self, log_source):
        self.db.execute_sql(self.log_table_create_statement.format(log_source))

    def get_available_log_sources(self):
        return self.db.get_table_names()

    def log(self, source, level, message):
        if source not in self.get_available_log_sources():
            raise LogSourceDoesNotExistException('Log Source {0} does not exist'.format(source))
        self.db.insert_row(table=source, row_string='(NULL, ?, ?, ?)', row_data=(int(time.time()), level, message))

    def get_all_logs(self, source):
        return [
            Log(source=source, timestamp=log[1], level=log[2], message=log[3]) for log in self.db.get_all_rows(table=source)
        ]
