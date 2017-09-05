import argparse
import time

from charitybot2.paths import production_repository_db_path
from charitybot2.persistence.donation_sqlite_repository import DonationSQLiteRepository
from charitybot2.sources.tiltify import TiltifySource


def get_donation_ids(donations):
    return [donation.internal_reference for donation in donations]


class TiltifyRunner:
    def __init__(self, event_identifier, repository_path, api_key, limit):
        self._tiltify = TiltifySource(event_identifier=event_identifier, api_key=api_key, limit=limit)
        self._event_identifier = event_identifier
        self._donations_repository = DonationSQLiteRepository(db_path=repository_path)
        self._tiltify_ids = []

    # Getting the stored donations from the donations service
    def get_stored_donations(self):
        return self._donations_repository.get_event_donations(event_identifier=self._event_identifier)

    def store_donation(self, donation):
        self._donations_repository.record_donation(donation=donation)

    def refill_cache(self):
        stored_ids = get_donation_ids(self.get_stored_donations())
        all_donations = self._tiltify.get_all_donations()
        all_tiltify_ids = get_donation_ids(all_donations)
        new_ids = [donation_id for donation_id in all_tiltify_ids if donation_id not in stored_ids]
        new_donations = [donation for donation in all_donations if donation.internal_reference in new_ids]
        for donation in new_donations:
            self.store_donation(donation=donation)

    def run_event_loop(self, delay):
        while True:
            current_timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            print('[{}]: Getting donations'.format(current_timestamp))
            known_donation_ids = [donation.id for donation in self.get_stored_donations()]
            new_donations = self._tiltify.get_new_donations(known_donation_ids=known_donation_ids)
            print('[{}]: {} known donations. {} new donations'.format(
                current_timestamp,
                len(known_donation_ids),
                len(new_donations)))
            for donation in new_donations:
                print('[{}] Storing donation of: {}{} from {}'.format(
                    current_timestamp,
                    '£',
                    donation.amount,
                    donation.donor_name
                ))
                self.store_donation(donation=donation)
            time.sleep(delay)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tiltify Runner')
    parser.add_argument(
        '-event',
        action='store',
        dest='event',
        help='Event Identifier')
    parser.add_argument(
        '-key',
        action='store',
        dest='api_key',
        help='Tiltify API Key')
    args = parser.parse_args()
    tiltify_runner = TiltifyRunner(
        event_identifier=args.event,
        repository_path=production_repository_db_path,
        api_key=args.api_key,
        limit=25
    )
