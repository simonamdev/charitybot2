from charitybot2.models.log import Log, LogLevel


class Logger:
    def __init__(self, source, event):
        self._source = source
        self._event = event

    def log(self, log):
        pass

    def log_verbose(self, timestamp, message):
        verbose_log = self._create_log(
            timestamp=timestamp,
            level=LogLevel.verbose,
            source=self._source,
            event=self._event,
            message=message)
        return self.log(log=verbose_log)

    def log_info(self, timestamp, message):
        info_log = self._create_log(
            timestamp=timestamp,
            level=LogLevel.info,
            source=self._source,
            event=self._event,
            message=message)
        return self.log(log=info_log)

    def log_warning(self, timestamp, message):
        info_log = self._create_log(
            timestamp=timestamp,
            level=LogLevel.warning,
            source=self._source,
            event=self._event,
            message=message)
        return self.log(log=info_log)

    def log_error(self, timestamp, message):
        info_log = self._create_log(
            timestamp=timestamp,
            level=LogLevel.error,
            source=self._source,
            event=self._event,
            message=message)
        return self.log(log=info_log)

    @staticmethod
    def _create_log(timestamp, level, source, event, message):
        return Log(timestamp=timestamp, level=level, source=source, event=event, message=message)
