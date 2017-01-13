import argparse

from charitybot2.events.donation import Donation
from charitybot2.storage.repository import Repository
from tests.tests import TestFilePath

donations_db_path = TestFilePath().get_db_path('donations.db')


def setup_parser():
    parser = argparse.ArgumentParser(description='Charitybot API Performance Test Setup')
    parser.add_argument('event', type=str, help='Event name for performance test')
    parser.add_argument('amount', type=int, help='Number of donations to be added for performance test')
    return parser

args = setup_parser().parse_args()
donations_db = Repository(db_path=donations_db_path, debug=True)
running_total = 0
for i in range(0, args.amount):
    next_donation = Donation(old_amount=running_total, new_amount=running_total + 5)
    running_total += 5
    donations_db.record_donation(event_name=args.event, donation=next_donation)
