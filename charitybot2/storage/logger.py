class LoggingFailedException(Exception):
    pass


class Logger:
    logging_service_url = service_full_url

    def __init__(self, source, event):
        self.source = source
        self.event = event

    # def log(self, level, messsage):
    #     try
