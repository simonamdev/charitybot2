from charitybot2.events.event_config import EventConfiguration
from charitybot2.storage.events_db import EventsDB, EventMetadata


class EventInvalidException(Exception):
    pass


class EventAlreadyFinishedException(Exception):
    pass


class Event:
    def __init__(self, config_path, db_handler):
        self.config_path = config_path
        self.db_handler = db_handler
        self.config = None
        self.amount_raised = 0
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
        self.db_handler.get_events_db().register_event(event_name=self.get_event_name())

    def get_event_current_state(self):
        return self.db_handler.get_events_db().get_event_state(event_name=self.get_event_name())

    def start_event(self):
        self.db_handler.get_events_db().change_event_state(
            event_name=self.get_event_name(),
            new_state=EventMetadata.ongoing_state)

    def stop_event(self):
        self.db_handler.get_events_db().change_event_state(
            event_name=self.get_event_name(),
            new_state=EventMetadata.completed_state)
