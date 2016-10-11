import charitybot2.events.event_config as event_config
import charitybot2.storage.events_db as storage

from charitybot2.events.event_config import EventConfiguration


class Event:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = None
        self.validate_config()

    def validate_config(self):
        self.config = EventConfiguration(file_path=self.config_path)
        self.config.read_config()

    def get_event_name(self):
        return self.config.get_config_value(value_name='name')

    def get_start_time(self):
        return self.config.get_config_value(value_name='start_time')

    def get_end_time(self):
        return self.config.get_config_value(value_name='end_time')

    def get_sources(self):
        return self.config.get_config_value(value_name='sources_required')

    def get_update_tick(self):
        return self.config.get_config_value(value_name='update_tick')


class EventLoop:
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
        self.db_interface.register_event(event_name=self.config.get_config_value('name'))

    def start_event(self):
        self.db_interface.change_event_state(
            event_name=self.config.get_config_value('name'),
            new_state=storage.EventsDB.event_ongoing_state)

    def stop_event(self):
        self.db_interface.change_event_state(
            event_name=self.config.get_config_value('name'),
            new_state=storage.EventsDB.event_completed_state
        )

    def check_for_donation(self):
        pass
