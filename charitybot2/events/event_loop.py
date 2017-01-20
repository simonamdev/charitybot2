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
        self.event_configuration = self.event.get_configuration()
        self.logger = Logger(
            source='EventLoop',
            event=self.event.name,
            console_only=debug)
        self.debug = debug
        self.scraper = None
        self.reporter = None
        self.loop_count = 0
        self.__initialise_scraper()
        self.__initialise_event_loop()

    def __initialise_scraper(self):
        source_url = self.event_configuration.get_source_url()
        if 'justgiving' in source_url:
            self.logger.log_info('Initialising JustGiving Scraper')
            self.scraper = JustGivingScraper(url=source_url)
        elif 'mydonate.bt' in source_url:
            self.logger.log_error('BTDonate scraper has not been implemented yet')
            raise NotImplementedError
        else:
            self.logger.log_error('Unable to initialise scraper for event: {}'.format(self.event.name))
            raise EventInvalidException('Unable to initialise scraper for event: {}'.format(self.event.name))

    def validate_event_loop(self):
        if self.event is None:
            raise EventInvalidException('No Event object passed to Event Loop')
        if time.time() > self.event.get_configuration().get_end_time():
            raise EventAlreadyFinishedException('Current time: {} Event end time: {}'.format(
                time.time(),
                self.event.get_configuration().get_end_time()))

    def __initialise_event_loop(self):
        self.logger.log_verbose('Checking whether the event is registered or not')
        self.__check_event_registration()
        self.logger.log_verbose('Checking whether the event already has donations')
        self.__check_for_donations()

    def __check_event_registration(self):
        if not self.__event_already_registered():
            self.logger.log_info('Registering event configuration')
            self.event.register_event()

    def __check_for_donations(self):
        if self.__donations_already_present():
            self.logger.log_verbose('Donations are already present for the event')
            # set the current amount from the last donation recorded
            last_donation = self.event.repository.get_last_donation(event_name=self.event.name)
            self.event.set_amount_raised(amount=last_donation.get_total_raised())
            self.logger.log_info('Amount raised retrieved from database is: {}{}'.format(
                self.event_configuration.get_currency().get_symbol(),
                self.event.get_amount_raised()
            ))
        else:
            self.logger.log_verbose('Donations are not present for the event')
            # set the current amount raised from the starting amount
            starting_amount = self.event.get_starting_amount()
            self.logger.log_info('Setting starting amount to: {}{}'.format(
                self.event_configuration.get_currency().get_key(),
                starting_amount))
            self.event.set_amount_raised(amount=starting_amount)

    def __donations_already_present(self):
        return self.event.repository.donations_are_present(event_name=self.event.name)

    def __event_already_registered(self):
        return self.event.repository.event_exists(event_name=self.event.name)

    def start(self):
        self.logger.log_info('Starting Event: {}'.format(self.event.name))
        while time.time() < self.event_configuration.get_end_time():
            hours_remaining = int((self.event_configuration.get_end_time() - time.time()) / (60 * 60))
            self.logger.log_info('Cycle {}: {} hours remaining in event'.format(
                self.loop_count,
                hours_remaining))
            self.check_for_donation()
            self.logger.log_info('Holding until cycle: {}'.format(self.loop_count + 1))
            time.sleep(self.event_configuration.get_update_delay())
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
        new_donation_detected = not new_amount == current_amount
        self.logger.log_info('Current Amount: {}, New Amount: {}, Donation detected: {}'.format(
            current_amount,
            new_amount,
            new_donation_detected))
        if new_donation_detected:
            self.logger.log_verbose('New donation detected')
            try:
                new_donation = Donation(old_amount=current_amount, new_amount=new_amount, timestamp=int(time.time()))
            except InvalidArgumentException:
                self.logger.log_error('These amounts do not match: Current Amount: {}, New Amount: {}'.format(
                    current_amount,
                    new_amount))
            else:
                self.event.set_amount_raised(amount=new_donation.get_total_raised())
                self.__record_new_donation(new_donation)
                self.report_new_donation(new_donation)

    def __record_new_donation(self, donation):
        self.logger.log_info('New Donation of {}{} detected'.format(
            self.event_configuration.get_currency().get_symbol(),
            donation.get_donation_amount()))
        self.event.repository.record_donation(event_name=self.event.name, donation=donation)

    def report_new_donation(self, donation):
        # This should be overridden by specific reporter children of this the EventLoop class
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
