import charitybot2.events.event_config as event_config
import charitybot2.storage.events_db as storage


class Event:
    def __init__(self, config_file_path, db_path):
        self.config_file_path = config_file_path
        self.db_path = db_path
        self.config = None
        self.db_interface = None
        self.validate_config()

    def validate_config(self):
        self.config = event_config.EventConfiguration(file_path=self.config_file_path)
        self.config.read_config()

    def initialise_db_interface(self):
        self.db_interface = storage.EventsDB(db_path=self.db_path)

    def register_event(self):
        pass
