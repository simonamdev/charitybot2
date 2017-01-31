class InvalidLogException(Exception):
    pass


class InvalidLogLevelException(InvalidLogException):
    pass


class LogLevel:
    verbose = 0
    info = 1
    warning = 2
    error = 3

    all_levels = (verbose, info, warning, error)


class Log:
    def __init__(self, timestamp, level, source, event, message):
        self._timestamp = timestamp
        self._level = level
        self._source = source
        self._event = event
        self._message = message

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def level(self):
        return self._level

    @property
    def source(self):
        return self._source

    @property
    def event(self):
        return self._event

    @property
    def message(self):
        return self._message

    def __validate_log(self):
        pass
        # if None in (self.timestamp, self.)
