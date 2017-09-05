import argparse
import os
import time

from charitybot2.api_calls.private_api_calls import PrivateApiCalls
from charitybot2.creators.event_configuration_creator import EventConfigurationCreatorFromFile
from charitybot2.paths import event_config_folder
from charitybot2.private_api.private_api import private_api_service
from charitybot2.sources.tiltify import TiltifySource


def get_donation_ids(donations):
    return [donation.internal_reference for donation in donations]

private_api_calls = PrivateApiCalls(base_api_url=private_api_service.full_url)


class TiltifyRunner:
    def __init__(self, event_identifier, api_key, limit):
        self._tiltify = TiltifySource(event_identifier=event_identifier, api_key=api_key, limit=limit)
        self._event_identifier = event_identifier
        self._tiltify_ids = []

    # Getting the stored donations from the donations service
    def get_stored_donations(self):
        return private_api_calls.get_event_donations(event_identifier=self._event_identifier)

    @staticmethod
    def store_donation(donation):
        private_api_calls.register_donation(donation=donation)

    def refill_cache(self):
        stored_ids = get_donation_ids(self.get_stored_donations())
        all_donations = self._tiltify.get_all_donations()
        all_tiltify_ids = get_donation_ids(all_donations)
        new_ids = [donation_id for donation_id in all_tiltify_ids if donation_id not in stored_ids]
        new_donations = [donation for donation in all_donations if donation.internal_reference in new_ids]
        for donation in new_donations:
            self.store_donation(donation=donation)

    def run_event_loop(self, delay):
        event_config_path = os.path.join(event_config_folder, 'onespecialday.json')
        event_config_creator = EventConfigurationCreatorFromFile(file_path=event_config_path)
        print('Registering event')
        private_api_calls.register_event(event_configuration=event_config_creator.configuration)
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
    parser.add_argument(
        '-delay',
        action='store',
        type=int,
        default=30,
        dest='delay',
        help='Tiltify API request delay')
    args = parser.parse_args()
    tiltify_runner = TiltifyRunner(
        event_identifier=args.event,
        api_key=args.api_key,
        limit=25
    )
    print('Starting Runner')
    tiltify_runner.run_event_loop(delay=args.delay)
