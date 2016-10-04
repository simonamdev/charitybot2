import os
import pytest

from charitybot2.storage.events_db import EventsDB

current_directory = os.path.dirname(os.path.abspath(__file__))
dummy_db_path = os.path.join(current_directory, 'db', 'dummy_events.db')
test_db_path = os.path.join(current_directory, 'db', 'test_events.db')

test_events = [
    'event_one',
    'event_two'
]


class TestEventsDBInitialisation:
    def test_initialising_db(self):
        edb = EventsDB(db_path=dummy_db_path, verbose=True)

    def test_events_db_is_created_when_it_does_not_exist(self):
        os.remove(dummy_db_path)
        edb = EventsDB(db_path=dummy_db_path, verbose=True)
        assert os.path.isfile(dummy_db_path) is True

    def test_event_exists(self):
        edb = EventsDB(db_path=test_db_path, verbose=True)
        assert edb.event_exists(event_name='event_one') is True
        assert edb.event_exists(event_name='dfjojsfdi') is False
