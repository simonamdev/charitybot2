from charitybot2.paths import init_event_log_script_path
from charitybot2.persistence.sql_script import SQLScript
from charitybot2.persistence.sqlite_repository import SQLiteRepository


class EventLogRepository(SQLiteRepository):
    def __init__(self, db_path='memory', debug=False):
        super().__init__(db_path=db_path, debug=debug)
        self.__validate_repository()

    def __validate_repository(self):
        init_script = SQLScript(path=init_event_log_script_path)
        self.execute_query(query=init_script.return_sql(), commit=True)
