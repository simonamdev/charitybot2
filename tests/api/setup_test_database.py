import random
import time
from faker import Faker

from charitybot2.creators.event_creator import EventRegister
from charitybot2.models.donation import Donation
from charitybot2.paths import test_repository_db_path
from charitybot2.persistence.donation_sqlite_repository import DonationSQLiteRepository
from charitybot2.persistence.event_sqlite_repository import EventSQLiteRepository
from tests.integration.test_event_register import get_test_event_configuration
from tests.mocks import WipeSQLiteDB


current_time = int(time.time())

updated_values = {
    'start_time': current_time,
    'end_time': current_time + 3600  # 1 hour long
}


def setup_test_database(event_values=None, donation_count=10):
    print('--- SETTING UP TEST DATABASE ---')
    wipe_database()
    if event_values is None:
        event_values = updated_values
    event_configuration = get_test_event_configuration(updated_values=event_values)
    register_event(event_configuration)
    register_donations(event_configuration=event_configuration, donation_count=donation_count)
    print('--- TEST DATABASE SETUP COMPLETE ---')


def wipe_database():
    print('Wiping old database')
    WipeSQLiteDB(db_path=test_repository_db_path).wipe_db()


def register_event(event_configuration):
    print('Registering event: {}'.format(event_configuration.identifier))
    event_repository = EventSQLiteRepository(db_path=test_repository_db_path)
    event_register = EventRegister(
        event_configuration=event_configuration,
        event_repository=event_repository)
    event_register.get_event()


def register_donations(event_configuration, donation_count):
    print('Recording donations')
    donations_repository = DonationSQLiteRepository(db_path=test_repository_db_path)
    shifting_time = current_time + 5
    fake = Faker()
    for i in range(0, donation_count + 1):
        print('Adding donation #{}'.format(i))
        shifting_time + random.randint(3, 20)
        donator_name = fake.name()
        donation = Donation(
            amount=round(random.uniform(1.0, 500.2), 2),
            event_identifier=event_configuration.identifier,
            timestamp=shifting_time,
            identifier='{}-{}'.format(shifting_time, donator_name),
            notes=donator_name)
        donations_repository.record_donation(donation=donation)
