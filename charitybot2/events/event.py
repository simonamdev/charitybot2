from charitybot2.events.event_config import EventConfiguration
from charitybot2.storage.events_db import EventsDB


class EventInvalidException(Exception):
    pass


class EventAlreadyFinishedException(Exception):
    pass


class Event:
    def __init__(self, config_path, db_path):
        self.config_path = config_path
        self.db_path = db_path
        self.db_interface = None
        self.config = None
        self.amount_raised = 0
        self.validate_config()
        self.initialise_db_interface()

    def validate_config(self):
        self.config = EventConfiguration(file_path=self.config_path)
        self.config.read_config()

    def initialise_db_interface(self):
        self.db_interface = EventsDB(db_path=self.db_path)

    def get_event_name(self):
        return self.config.get_config_value(value_name='name')

    def get_start_time(self):
        return self.config.get_config_value(value_name='start_time')

    def get_end_time(self):
        return self.config.get_config_value(value_name='end_time')

    def get_target_amount(self):
        return self.config.get_config_value(value_name='target_amount')

    def get_source_url(self):
        return self.config.get_config_value(value_name='source_url')

    def get_update_tick(self):
        return self.config.get_config_value(value_name='update_tick')

    def set_amount_raised(self, amount):
        self.amount_raised = amount

    def increment_amount_raised(self, amount_increase):
        self.amount_raised += amount_increase

    def get_amount_raised(self):
        return self.amount_raised

    def register_event(self):
        self.db_interface.register_event(event_name=self.get_event_name())

    def get_event_current_state(self):
        return self.db_interface.get_event_state(event_name=self.get_event_name())

    def start_event(self):
        self.db_interface.change_event_state(
            event_name=self.get_event_name(),
            new_state=EventsDB.event_ongoing_state)

    def stop_event(self):
        self.db_interface.change_event_state(
            event_name=self.get_event_name(),
            new_state=EventsDB.event_completed_state)
