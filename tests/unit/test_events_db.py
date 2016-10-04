import os
import pytest

from charitybot2.storage.events_db import EventsDB

current_directory = os.path.dirname(os.path.abspath(__file__))
test_db_path = os.path.join(current_directory, 'db', 'test_events.db')


class TestEventsDBInitialisation:
    def test_initialising_db(self):
        edb = EventsDB(db_path=test_db_path, verbose=True)

    def test_events_db_is_created_when_it_does_not_exist(self):
        os.remove(test_db_path)
        edb = EventsDB(db_path=test_db_path, verbose=True)
        assert os.path.isfile(test_db_path) is True
