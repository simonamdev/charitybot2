import time

from charitybot2.models.event_log import EventLog
from pypika import Query, Table, functions as fn

from charitybot2.paths import init_event_log_script_path
from charitybot2.persistence.sql_script import SQLScript
from charitybot2.persistence.sqlite_repository import SQLiteRepository


def fix_placeholders(query):
    return str(query).replace('\'', '')


class EventLogRepository(SQLiteRepository):
    def __init__(self, db_path='memory', debug=False):
        super().__init__(db_path=db_path, debug=debug)
        self._event_log_table = Table('eventLog')
        self.__validate_repository()

    def __validate_repository(self):
        init_script = SQLScript(path=init_event_log_script_path)
        self.execute_query(query=init_script.return_sql(), commit=True)

    def get_logged_events(self):
        q = Query.from_(self._event_log_table).select('internalName')
        rows = self.execute_query(query=fix_placeholders(q)).fetchall()
        return [self.__convert_row_to_event_log(row) for row in rows]

    @staticmethod
    def __convert_row_to_event_log(row):
        return EventLog(event_identifier=row[0], last_log_time=row[1])
