class EventLog:
    def __init__(self, event_identifier, last_log_time):
        self._event_identifier = event_identifier
        self._last_log_time = last_log_time

    @property
    def identifier(self):
        return self._event_identifier

    @property
    def last_log_time(self):
        return self._last_log_time
