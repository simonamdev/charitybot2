import os
import pytest

from charitybot2.storage.events_db import EventsDB, EventAlreadyRegisteredException, EventGivenInvalidStateException
from tests.tests import ResetDB

current_directory = os.path.dirname(os.path.abspath(__file__))
test_db_path = os.path.join(current_directory, 'db', 'test_events.db')
events_db_path = os.path.join(current_directory, 'db', 'test_events.db')
events_db_init_script_path = os.path.join(current_directory, 'db', 'init_test_events.sql')

test_events = [
    'event_one',
    'event_two'
]

ResetDB(db_path=test_db_path, sql_path=events_db_init_script_path)


class TestEventsDBInitialisation:
    def test_initialising_db(self):
        edb = EventsDB(db_path=test_db_path, debug=True)


class TestEventDBRetrieve:
    def test_event_exists(self):
        edb = EventsDB(db_path=test_db_path, debug=True)
        assert edb.event_exists(event_name='event_one') is True
        assert edb.event_exists(event_name='dfjojsfdi') is False

    def test_get_all_event_names(self):
        edb = EventsDB(db_path=test_db_path, debug=True)
        assert sorted(test_events) == sorted(edb.get_all_event_names())

    def test_get_event_metadata(self):
        edb = EventsDB(db_path=test_db_path, debug=True)
        data = edb.get_event_metadata(event_name='event_two')
        assert data == {
            'name': 'event_two',
            'uuid': '123457',
            'state': EventsDB.event_default_state
        }


class TestEventDBCreate:
    def test_register_event_already_registered_throws_exception(self):
        edb = EventsDB(db_path=test_db_path, debug=True)
        with pytest.raises(EventAlreadyRegisteredException):
            edb.register_event(event_name='event_one')

    def test_register_event_successfully_stores_in_db(self):
        edb = EventsDB(db_path=test_db_path, debug=True)
        edb.register_event(event_name='new_event_one')
        assert edb.event_exists(event_name='new_event_one')

    def test_new_events_default_state_is_correct(self):
        edb = EventsDB(db_path=test_db_path, debug=True)
        edb.register_event(event_name='new_event_two')
        data = edb.get_event_metadata(event_name='new_event_two')
        assert data['state'] == EventsDB.event_default_state

    def test_successful_event_state_change(self):
        edb = EventsDB(db_path=test_db_path, debug=True)
        edb.change_event_state(event_name='event_one', new_state='ONGOING')
        data = edb.get_event_metadata(event_name='event_one')
        assert data['state'] == 'ONGOING'

    def test_event_state_change_to_nonexistent_throws_exception(self):
        edb = EventsDB(db_path=test_db_path, debug=True)
        with pytest.raises(EventGivenInvalidStateException):
            edb.change_event_state(event_name='event_one', new_state='GARBAGE')
