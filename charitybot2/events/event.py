from charitybot2.config.event_config import EventConfiguration
from charitybot2.events.currency import Currency


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
        return self.config.get_value('event_name')

    def get_channel_name(self):
        return self.config.get_value('channel_name')

    def get_start_time(self):
        return self.config.get_value('start_time')

    def get_end_time(self):
        return self.config.get_value('end_time')

    def get_target_amount(self):
        return self.config.get_value('target_amount')

    def get_source_url(self):
        return self.config.get_value('source_url')

    def get_update_tick(self):
        return self.config.get_value('update_tick')

    def set_amount_raised(self, amount):
        self.amount_raised = amount

    def increment_amount_raised(self, amount_increase):
        self.amount_raised += amount_increase

    def get_amount_raised(self):
        return self.amount_raised

    def get_currency(self):
        return Currency(self.config.get_value('currency'))

    def register_currency_key(self):
        if not self.db_handler.get_donations_db().currency_is_set(event_name=self.get_event_name()):
            self.db_handler.get_donations_db().set_event_currency_key(
                event_name=self.get_event_name(),
                currency_key=self.get_currency().get_key())
