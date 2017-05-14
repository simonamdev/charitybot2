import time

from charitybot2.creators.event_creator import EventRegister
from charitybot2.paths import test_repository_db_path
from charitybot2.persistence.event_sqlite_repository import EventSQLiteRepository
from tests.integration.test_event_register import get_test_event_configuration
from tests.mocks import WipeSQLiteDB


current_time = int(time.time())

updated_values = {
    'start_time': current_time,
    'end_time': current_time + 3600  # 1 hour long
}
default_event_configuration = get_test_event_configuration(updated_values=updated_values)


def setup_test_database(event_values=None, donation_count=10):
    print('--- SETTING UP TEST DATABASE ---')
    wipe_database()
    register_event(event_values)
    register_donations(donation_count=donation_count)
    print('--- TEST DATABASE SETUP COMPLETE ---')


def wipe_database():
    print('Wiping old database')
    WipeSQLiteDB(db_path=test_repository_db_path).wipe_db()


def register_event(event_values):
    if event_values is None:
        event_values = updated_values
    event_configuration = get_test_event_configuration(updated_values=event_values)
    print('Registering event: {}'.format(event_configuration.identifier))
    event_repository = EventSQLiteRepository(db_path=test_repository_db_path)
    event_register = EventRegister(
        event_configuration=event_configuration,
        event_repository=event_repository)
    event_register.get_event()


def register_donations(donation_count):
    pass
