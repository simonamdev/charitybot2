import time

from charitybot2.storage.events_db import EventsDB
from charitybot2.events.event_config import EventConfiguration, InvalidEventConfigException
from charitybot2.sources.justgiving import JustGivingScraper


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


class EventLoop:
    def __init__(self, event, verbose=False):
        self.event = event
        self.verbose = verbose
        self.scraper = None
        self.loop_count = 0
        self.validate_event_loop()
        self.initialise_scraper()

    def log(self, log_string):
        if self.verbose:
            print('[{}] [EL] {}'.format(int(time.time()), log_string))

    def validate_event_loop(self):
        if self.event is None:
            raise EventInvalidException('No Event object passed to Event Loop')
        if time.time() > self.event.get_end_time():
            raise EventAlreadyFinishedException('Current time: {} Event end time: {}'.format(time.time(), self.event.get_end_time()))

    def initialise_scraper(self):
        source_url = self.event.get_source_url()
        if 'justgiving' in source_url:
            self.log('Initialising JustGiving Scraper')
            self.scraper = JustGivingScraper(url=source_url)
        elif 'mydonate.bt' in source_url:
            raise NotImplementedError
        else:
            raise EventInvalidException

    def start(self):
        self.log('Registering Event: {}'.format(self.event.get_event_name()))
        self.event.register_event()
        self.log('Starting Event: {}'.format(self.event.get_event_name()))
        self.event.start_event()
        while time.time() < self.event.get_end_time():
            hours_remaining = int((self.event.get_end_time() - time.time()) / (60 * 60))
            self.log('Cycle {}: {} hours remaining in event'.format(
                self.loop_count,
                hours_remaining))
            time.sleep(self.event.get_update_tick())
        self.event.stop_event()

    def get_current_amount_raised(self):
        self.event.set_amount_raised(amount=self.scraper.get_amount_raised())
