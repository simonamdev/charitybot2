import time

from charitybot2.paths import production_logs_db_path
from charitybot2.storage.logs_db import Log, LogsDB
from colorama import Style
from colorama import init, Fore


class LoggingFailedException(Exception):
    pass


class Logger:
    def __init__(self, source, event, debug_db_path='', console_only=False):
        init()
        self.source = source
        self.event = event
        self.debug_db_path = debug_db_path
        self.console_only = console_only
        self.logs_db = None
        if not self.console_only:
            self.initialise_db_connection()

    def initialise_db_connection(self):
        db_path = production_logs_db_path
        if self.debug_db_path is not '':
            db_path = self.debug_db_path
        self.logs_db = LogsDB(db_path=db_path, verbose=False)

    def log_verbose(self, message):
        self.log(level=Log.verbose_level, message=message)

    def log_info(self, message):
        self.log(level=Log.info_level, message=message)

    def log_warning(self, message):
        self.log(level=Log.warning_level, message=message)

    def log_error(self, message):
        self.log(level=Log.error_level, message=message)

    def log(self, level, message):
        self.log_to_console(level=level, message=message)
        if not self.console_only:
            return self.log_to_db(level=level, message=message)

    def log_to_console(self, level, message):
        console_log = Log(source=self.source, event=self.event, timestamp=int(time.time()), level=level, message=message)
        if level == Log.error_level:
            print(Fore.RED + str(console_log))
            print(Style.RESET_ALL)
        else:
            print(console_log)

    def log_to_db(self, level, message):
        self.logs_db.log(source=self.source, event=self.event, level=level, message=message)
