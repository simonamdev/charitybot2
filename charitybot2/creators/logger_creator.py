"""
Depending on the debug flag, the LoggerCreator will return either a RepositoryLogger or a ConsoleLogger
"""
from charitybot2.models.log import Log
from charitybot2.persistence.console_logger import ConsoleLogger
from charitybot2.persistence.repository_logger import RepositoryLogger


class LoggerCreator:
    def __init__(self, debug=False):
        self._debug = debug

    @property
    def debug(self):
        return self._debug

    def get_logger(self):
        if self.debug:
            return ConsoleLogger()
        else:
            return RepositoryLogger()


class Logger:
    def log(self, log):
        pass

    def log_verbose(self, timestamp, source, ):
        verbose_log = self._create_log()

    def log_info(self):
        pass

    @staticmethod
    def _create_log(timestamp, level, source, event, message):
        return Log(timestamp=timestamp, level=level, source=source, event=event, message=message)
