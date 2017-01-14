import time

from charitybot2.events.donation import Donation, InvalidArgumentException
from charitybot2.events.event import EventInvalidException, EventAlreadyFinishedException
from charitybot2.reporter.twitch import ChatBot
from charitybot2.sources.justgiving import JustGivingScraper
from charitybot2.sources.scraper import SourceUnavailableException
from charitybot2.storage.logger import Logger


class EventLoop:
    def __init__(self, event, debug=False):
        self.event = event
        self.validate_event_loop()
        self.logger = Logger(source='EventLoop', event=self.event.get_internal_name(), console_only=debug)
        self.debug = debug
        self.scraper = None
        self.reporter = None
        self.loop_count = 0
        self.donation_checks = 0
        self.initialise_scraper()
        self.initialise_event_loop()

    def validate_event_loop(self):
        if self.event is None:
            raise EventInvalidException('No Event object passed to Event Loop')
        if time.time() > self.event.get_end_time():
            raise EventAlreadyFinishedException('Current time: {} Event end time: {}'.format(
                time.time(),
                self.event.get_end_time()))

    def initialise_event_loop(self):
        self.logger.log_verbose('Registering/Updating event configuration')
        self.event.register_or_update_event()
        self.logger.log_verbose('Checking whether the event already has donations')
        if self.donations_already_present():
            # set the current amount from the last donation recorded
            last_donation = self.event.repository.get_last_donation(event_name=self.event.get_internal_name())
            self.event.set_amount_raised(last_donation.get_total_raised())
            self.logger.log_info('Amount raised retrieved from database is: {}{}'.format(
                self.event.get_currency().get_symbol(),
                self.event.get_amount_raised()
            ))

    def donations_already_present(self):
        if not self.event_already_registered():
            return False
        return self.event.repository.get_number_of_donations(event_name=self.event.get_internal_name()) > 0

    def event_already_registered(self):
        return self.event.repository.event_exists(event_name=self.event.get_internal_name())

    def initialise_scraper(self):
        source_url = self.event.get_source_url()
        if 'justgiving' in source_url:
            self.logger.log_info('Initialising JustGiving Scraper')
            self.scraper = JustGivingScraper(url=source_url)
        elif 'mydonate.bt' in source_url:
            self.logger.log_error('BTDonate scraper has not been implemented yet')
            raise NotImplementedError
        else:
            self.logger.log_error('Unable to initialise scraper for event: {}'.format(self.event.get_internal_name()))
            raise EventInvalidException('Unable to initialise scraper for event: {}'.format(self.event.get_internal_name()))

    def start(self):
        self.logger.log_info('Starting Event: {}'.format(self.event.get_internal_name()))
        while time.time() < self.event.get_end_time():
            hours_remaining = int((self.event.get_end_time() - time.time()) / (60 * 60))
            self.logger.log_info('Cycle {}: {} hours remaining in event'.format(
                self.loop_count,
                hours_remaining))
            self.check_for_donation()
            self.logger.log_info('Holding until cycle: {}'.format(self.loop_count + 1))
            time.sleep(self.event.get_update_tick())
            self.loop_count += 1
        self.logger.log_info('Event has exceeded its end time')

    def get_new_amount(self):
        try:
            new_amount = self.scraper.scrape_amount_raised()
        except SourceUnavailableException:
            self.logger.log_error('Unable to connect to donation website')
            return ''
        # convert the string to a float, removing any currency symbols and commas
        return float(new_amount.replace(',', '').replace('£', '').replace('$', '').replace('€', ''))

    def check_for_donation(self):
        current_amount = float(self.event.get_amount_raised())
        new_amount = self.get_new_amount()
        if new_amount == '':
            self.logger.log_error('Could not check for donation, skipping cycle')
            return
        self.logger.log_info('Current Amount: {}, New Amount: {}'.format(current_amount, new_amount))
        new_donation_detected = not new_amount == current_amount
        if new_donation_detected and not self.donation_checks == 0:
            self.logger.log_verbose('New donation detected')
            try:
                new_donation = Donation(old_amount=current_amount, new_amount=new_amount, timestamp=int(time.time()))
            except InvalidArgumentException:
                self.logger.log_error('These do not match: Current Amount: {}, New Amount: {}'.format(current_amount, new_amount))
            else:
                self.event.set_amount_raised(amount=new_donation.get_total_raised())
                self.record_new_donation(new_donation)
                self.report_new_donation(new_donation)
        self.donation_checks += 1

    def record_new_donation(self, donation):
        self.logger.log_info('New Donation of {} {} detected'.format(
            self.event.get_currency().get_key(),
            donation.get_donation_amount()))
        self.event.repository.record_donation(event_name=self.event.get_internal_name(), donation=donation)

    def report_new_donation(self, donation):
        pass


class TwitchEventLoop(EventLoop):
    def __init__(self, event, twitch_account, debug=False):
        super().__init__(event=event, debug=debug)
        self.twitch_account = twitch_account
        self.initialise_reporter()

    def initialise_reporter(self):
        self.twitch_account.validate_twitch_account()
        self.reporter = ChatBot(
            twitch_account=self.twitch_account,
            event=self.event,
            debug=self.debug)

    def report_new_donation(self, donation):
        self.reporter.post_donation_to_chat(donation=donation)
