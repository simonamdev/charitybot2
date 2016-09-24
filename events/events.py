import events.event_config as event_config


class Event:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.config = None
        self.read_config()

    def read_config(self):
        self.config = event_config.EventConfiguration(file_path=self.config_file_path)
