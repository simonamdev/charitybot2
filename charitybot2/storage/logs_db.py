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

    def get_source(self):
        return self.source

    def get_event(self):
        return self.event


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

    def convert_row_to_log(self, row):
        return Log(source=row[3], timestamp=row[1], level=row[2], message=row[5], event=row[4])

    def get_all_logs(self):
        return [
            self.convert_row_to_log(log) for log in self.db.get_all_rows(table='logs')
        ]

    def get_specific_logs(self, time='', level='', source='', event=''):
        # build filter string
        filter_string = ''
        if not time == '':
            filter_string += 'time > {} AND '.format(time)
        if not level == '':
            filter_string += 'level = {} AND '.format(level)
        if not source == '':
            filter_string += 'source = "{}" AND '.format(source)
        if not event == '':
            filter_string += 'event = "{}" AND '.format(event)
        filter_string += 'id IS NOT NULL;'
        # filtered_logs = self.db.get_specific_rows(table='logs', filter_string=filter_string)
        filtered_logs = self.db.get_specific_rows(table='logs', filter_string=filter_string)
        return [
            self.convert_row_to_log(log) for log in filtered_logs
        ]
