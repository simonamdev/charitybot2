import time
import datetime

from charitybot2.storage.base_db import BaseDB


class Log:
    info_level = 0
    warning_level = 1
    error_level = 2

    def __init__(self, source, timestamp, level, event, message):
        self.source = source
        self.timestamp = timestamp
        self.level = level
        self.event = event
        self.message = message

    def __str__(self):
        return '[{}] [{}] [{}] [{}]: {}'.format(
            datetime.datetime.fromtimestamp(self.timestamp).strftime('%H:%M:%S'),
            self.level,
            self.source,
            self.event,
            self.message
        )

    def get_time(self):
        return self.timestamp

    def get_message(self):
        return self.message

    def get_level(self):
        return self.level


class LogsDB(BaseDB):
    logs_table_create_statement = 'CREATE TABLE IF NOT EXISTS `logs` (' \
                                 '`id`	    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,' \
                                 '`time`	INTEGER NOT NULL,' \
                                 '`level`	INTEGER NOT NULL DEFAULT 0,' \
                                 '`source`  TEXT NOT NULL,' \
                                 '`event`	TEXT NOT NULL,' \
                                 '`message` TEXT NOT NULL' \
                                 ');'

    def __init__(self, db_path, verbose=False):
        super().__init__(file_path=db_path, db_name='Logs DB', verbose=verbose)
        self.initialise()
        self.create_log_source_table()

    def create_log_source_table(self):
        self.db.execute_sql(self.logs_table_create_statement)

    def log(self, source, event, level, message):
        self.db.insert_row(
            table='logs',
            row_string='(NULL, ?, ?, ?, ?, ?)',
            row_data=(int(time.time()), level, source, event, message)
        )

    def get_all_logs(self):
        return [
            Log(source=log[3], timestamp=log[1], level=log[2], message=log[4], event=log[5]) for log in self.db.get_all_rows(table='logs')
        ]
