import datetime
from colorama import Style, Fore
from colorama import init as init_colorama


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

    level_names = (
        'VERBOSE',
        'INFO',
        'WARNING',
        'ERROR'
    )


class Log:
    def __init__(self, timestamp, level, source, event, message):
        self._timestamp = timestamp
        self._level = level
        self._source = source
        self._event = event
        self._message = message
        self.__validate_log()
        init_colorama()

    def __str__(self):
        readable_timestamp = datetime.datetime.fromtimestamp(self.timestamp).strftime('%H:%M:%S')
        abbreviated_level = LogLevel.level_names[self.level][0:3]
        abbreviated_source = self.source[0:5]
        abbreviated_event = self.event[0:5]
        log_string = '[{}]-[{}]-[{}]-[{}]: {}'.format(
            readable_timestamp,
            abbreviated_level,
            abbreviated_source,
            abbreviated_event,
            self._message)
        if len(log_string) >= 80:
            log_string = log_string[:80]
        if self.level == LogLevel.error:
            log_string = Fore.RED + log_string + Style.RESET_ALL
        return log_string

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
        if self.timestamp is None or self.timestamp < 0:
            raise InvalidLogException('Timestamp value cannot be invalid (less than zero or null)')
        if self.level not in LogLevel.all_levels:
            raise InvalidLogLevelException('Log Level passed is invalid')
        if '' in (self.source, self.event, self.message):
            raise InvalidLogException('No Log parameters can be empty strings')
        if None in (self.timestamp, self.level, self.source, self.event, self.message):
            raise InvalidLogException('No Log parameters can be null')
