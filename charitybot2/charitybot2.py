import time

from charitybot2.events.donation import Donation
from charitybot2.events.event import EventInvalidException, EventAlreadyFinishedException
from charitybot2.sources.justgiving import JustGivingScraper
from charitybot2.storage.logger import Logger


class EventLoop:
    def __init__(self, event, twitch_account, debug=False):
        self.event = event
        self.debug = debug
        self.scraper = None
        self.loop_count = 0
        self.logger = Logger(source='EventLoop', console_only=debug)
        self.validate_event_loop()
        self.initialise_scraper()

    def validate_event_loop(self):
        if self.event is None:
            raise EventInvalidException('No Event object passed to Event Loop')
        if time.time() > self.event.get_end_time():
            raise EventAlreadyFinishedException('Current time: {} Event end time: {}'.format(time.time(), self.event.get_end_time()))

    def initialise_scraper(self):
        source_url = self.event.get_source_url()
        if 'justgiving' in source_url:
            self.logger.log_info('Initialising JustGiving Scraper')
            self.scraper = JustGivingScraper(url=source_url)
        elif 'mydonate.bt' in source_url:
            raise NotImplementedError
        else:
            raise EventInvalidException

    def initialise_reporter(self):
        pass

    def start(self):
        self.logger.log_info('Registering Event: {}'.format(self.event.get_event_name()))
        self.event.register_event()
        self.logger.log_info('Starting Event: {}'.format(self.event.get_event_name()))
        self.event.start_event()
        while time.time() < self.event.get_end_time():
            hours_remaining = int((self.event.get_end_time() - time.time()) / (60 * 60))
            self.logger.log_info('Cycle {}: {} hours remaining in event'.format(
                self.loop_count,
                hours_remaining))
            self.check_for_donation()
            time.sleep(self.event.get_update_tick())
            self.loop_count += 1
        self.event.stop_event()

    def check_for_donation(self):
        current_amount = self.event.get_amount_raised()
        new_amount = self.scraper.get_amount_raised()
        if not new_amount == current_amount:
            self.record_new_donation(Donation(current_amount, new_amount))

    def record_new_donation(self, donation):
        self.logger.log_info('New Donation of £{} detected'.format(donation.get_donation_amount()))
        self.event.set_amount_raised(amount=donation.get_new_amount())
        self.event.db_handler.get_donations_db().record_donation(event_name=self.event.get_event_name(), donation=donation)

    def report_new_donation(self, donation):
        pass
