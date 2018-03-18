import random
import time

import sqlite3
from faker import Faker
from tqdm import tqdm

from charitybot2.creators.event_creator import EventRegister
from charitybot2.models.donation import Donation
from charitybot2.paths import test_repository_db_path
from charitybot2.persistence.donation_sqlite_repository import DonationSQLiteRepository
from charitybot2.persistence.event_sqlite_repository import EventSQLiteRepository
from helpers.event_config import get_test_event_configuration

current_time = int(time.time())
# 2 hours long
start_time = current_time - 3600
end_time = current_time + 3600

updated_values = {
    'start_time': start_time,
    'end_time': end_time
}

# TODO: Refactor these helper functions


class WipeSQLiteDB:
    def __init__(self, db_path):
        self._db_path = db_path

    def wipe_db(self):
        print('Wiping database at path: {}'.format(self._db_path))
        enable_pragma_query = 'PRAGMA writable_schema = 1;'
        delete_query = 'DELETE FROM sqlite_master WHERE type IN ("table", "index", "trigger");'
        disable_pragma_query = 'PRAGMA writeable_schema = 0;'
        vacuum_query = 'VACUUM;'
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        for query in (enable_pragma_query, delete_query, disable_pragma_query, vacuum_query):
            print('Executing: {}'.format(query))
            cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()
        print('Wipe complete')


def setup_test_database(event_values=None, donation_count=10, donation_amount=None, db_path=None):
    if db_path is None:
        db_path = test_repository_db_path
    print('--- SETTING UP TEST DATABASE ---')
    wipe_database(db_path)
    if event_values is None:
        event_values = updated_values
    event_configuration = get_test_event_configuration(updated_values=event_values)
    register_test_event(db_path, event_configuration)
    donations = register_donations(
        db_path=db_path,
        event_configuration=event_configuration,
        donation_count=donation_count,
        donation_amount=donation_amount)
    print('--- TEST DATABASE SETUP COMPLETE ---')
    # return the donations for reference in tests
    return donations


def wipe_database(path):
    print('Wiping database at path: {}'.format(path))
    if not path == test_repository_db_path:
        for i in range(5, 0, -1):
            print('Wiping in: {}'.format(i))
            time.sleep(1)
    WipeSQLiteDB(db_path=path).wipe_db()


def register_test_event(db_path, event_configuration):
    print('Registering event: {}'.format(event_configuration.identifier))
    event_repository = EventSQLiteRepository(db_path=db_path)
    event_register = EventRegister(
        event_configuration=event_configuration,
        event_repository=event_repository)
    event_register.get_event()


def register_donations(db_path, event_configuration, donation_count, donation_amount):
    # TODO: Refactor this!
    randomise_donations = False
    if donation_amount is None:
        randomise_donations = True
    print('Recording donations')
    donations_repository = DonationSQLiteRepository(db_path=db_path)
    shifting_time = start_time + 5
    fake = Faker()
    print('Adding {} donations'.format(donation_count))
    total = 0
    donations = []
    for i in tqdm(range(0, donation_count)):
        shifting_time += random.randint(5, 60)
        donor_name = fake.name()
        if randomise_donations:
            donation_amount = round(random.uniform(1.0, 100.0), 2)
            total += donation_amount
        donation = Donation(
            amount=donation_amount,
            timestamp=shifting_time,
            event_identifier=event_configuration.identifier,
            external_reference='N/A',
            notes='N/A',
            donor_name=donor_name)
        donations.append(donation)
        donations_repository.record_donation(donation=donation)
    # set the total
    print('Setting total to: {}'.format(total))
    events_repository = EventSQLiteRepository(db_path=db_path)
    events_repository.update_event_current_amount(identifier='test', current_amount=round(total, 2))
    return donations


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        setup_test_database(donation_count=int(sys.argv[1]))
    elif len(sys.argv) == 3:
        print('Database at path: {} will be wiped'.format(sys.argv[2]))
        input('Are you sure?')
        input('ARE YOU DEFINITELY SURE?')
        setup_test_database(donation_count=int(sys.argv[1]), db_path=sys.argv[2])
    else:
        setup_test_database()
