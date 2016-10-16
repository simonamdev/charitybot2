from charitybot2.storage.events_db import EventsDB
from charitybot2.events.event_config import EventConfiguration, InvalidEventConfigException
from charitybot2.sources.justgiving import JustGivingScraper


class EventInvalidException(Exception):
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

    def start_event(self):
        self.db_interface.change_event_state(
            event_name=self.get_event_name(),
            new_state=EventsDB.event_ongoing_state)

    def stop_event(self):
        self.db_interface.change_event_state(
            event_name=self.get_event_name(),
            new_state=EventsDB.event_completed_state)


class EventLoop:
    def __init__(self, event):
        self.event = event
        self.scraper = None
        self.validate_event_loop()
        self.initialise_scraper()

    def validate_event_loop(self):
        if self.event is None:
            raise EventInvalidException('No Event object passed to Event Loop')

    def initialise_scraper(self):
        source_url = self.event.get_source_url()
        if 'justgiving' in source_url:
            self.scraper = JustGivingScraper(url=source_url)
        elif 'mydonate.bt' in source_url:
            raise NotImplementedError
        else:
            raise EventInvalidException

    def start_loop(self):
        pass

    def get_current_amount_raised(self):
        self.event.set_amount_raised(amount=self.scraper.get_amount_raised())

