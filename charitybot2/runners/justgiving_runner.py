import argparse
import time

from charitybot2.creators.event_configuration_creator import EventConfigurationCreatorFromFile
from charitybot2.persistence.donation_sqlite_repository import DonationSQLiteRepository
from charitybot2.persistence.event_sqlite_repository import EventSQLiteRepository
from charitybot2.sources.justgiving import JustGivingFundraisingSource

db_path = '../data/db/repository.db'


class JustgivingRunner:
    def __init__(self, event_config_path, page_short_name, api_key, limit=100):
        self._event_configuration = None
        self._event_config_path = event_config_path
        self._page_short_name = page_short_name
        self._source = None
        self._api_key = api_key
        self._external_references = []
        self._limit = limit
        self._event_repository = EventSQLiteRepository(db_path=db_path)
        self._donation_repository = DonationSQLiteRepository(db_path=db_path)
        self.register_event()
        self.setup_source()

    # Register the event with the event service
    def register_event(self):
        print('Registering event')
        event_config_creator = EventConfigurationCreatorFromFile(file_path=self._event_config_path)
        self._event_configuration = event_config_creator.configuration
        self._event_repository.register_event(event_configuration=self._event_configuration)


    def setup_source(self):
        self._source = JustGivingFundraisingSource(
            event_identifier=self._event_configuration.identifier,
            page_short_name=self._page_short_name,
            api_key=self._api_key,
            limit=self._limit
        )

    # Getting the stored donations from the donations service
    def get_stored_donations(self):
        return self._donation_repository.get_event_donations(event_identifier=self._event_configuration.identifier)

    def store_donation(self, donation):
        self._donation_repository.record_donation(donation=donation)

    def update_total(self, total):
        self._event_repository.update_event_current_amount(identifier=self._event_configuration.identifier, current_amount=total)

    # run the event loop
    def run_event_loop(self, delay):
        current_total = 0.0
        while True:
            current_timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            print('[{}]: Getting donations'.format(current_timestamp))
            known_donation_ids = [donation.external_reference for donation in self.get_stored_donations()]
            new_donations = self._source.get_new_donations(known_donation_ids=known_donation_ids)
            if new_donations is None:
                print('[{}]: Unable to retrieve donations. Skipping cycle'.format(current_timestamp))
                continue
            print('[{}]: {} known donations. {} new donations'.format(
                current_timestamp,
                len(known_donation_ids),
                len(new_donations)))
            for donation in new_donations:
                print('[{}]: Storing donation of: {} {} from {}'.format(
                    current_timestamp,
                    self._event_configuration.currency.key,
                    donation.amount,
                    donation.donor_name
                ))
                self.store_donation(donation=donation)
            # update the total because just giving provide it in a separate part
            print('[{}]: Getting total'.format(current_timestamp))
            new_total = self._source.get_total_raised()
            if not new_total == current_total:
                print('[{}]: Setting new total: {}'.format(current_timestamp, new_total))
                self.update_total(new_total)
                current_total = new_total
            print('[{}]: Next cycle in: {} seconds'.format(current_timestamp, delay))
            time.sleep(delay)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='JustGiving Runner')
    parser.add_argument(
        '-event-config',
        action='store',
        dest='event_config_path',
        help='Event Config File Path')
    parser.add_argument(
        '-name',
        action='store',
        dest='short_page_name',
        help='Event short page name')
    parser.add_argument(
        '-key',
        action='store',
        dest='api_key',
        help='JustGiving API Key')
    parser.add_argument(
        '-delay',
        action='store',
        type=int,
        default=30,
        dest='delay',
        help='JustGiving API request delay')
    args = parser.parse_args()
    justgiving_runner = JustgivingRunner(
        event_config_path=args.event_config_path,
        api_key=args.api_key,
        page_short_name=args.short_page_name,
        limit=25
    )
    print('Starting Runner')
    justgiving_runner.run_event_loop(delay=args.delay)
