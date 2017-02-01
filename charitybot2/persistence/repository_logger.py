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
        super().__init__(source=source, event=event)

    def log(self, log):
        self._console_logger.log(log=log)
        self.__store_log_in_repository(log=log)

    def __store_log_in_repository(self, log):
        log_storage_query = ''

    def get_all_logs(self):
        pass

    def get_specific_logs(self, timestamp=None, level=None, source=None, event=None):
        pass
