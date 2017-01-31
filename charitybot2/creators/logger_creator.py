"""
Depending on the debug flag, the LoggerCreator will return either a RepositoryLogger or a ConsoleLogger
"""
from charitybot2.persistence.console_logger import ConsoleLogger
from charitybot2.persistence.repository_logger import RepositoryLogger


class LoggerCreator:
    def __init__(self, source, event, debug=False):
        self._source = source
        self._event = event
        self._debug = debug

    @property
    def debug(self):
        return self._debug

    def get_logger(self):
        if self.debug:
            return ConsoleLogger(source=self._source, event=self._event)
        else:
            return RepositoryLogger(source=self._source, event=self._event)
