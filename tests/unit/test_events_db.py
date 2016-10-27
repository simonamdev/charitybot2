import pytest

from charitybot2.storage.events_db import EventsDB, EventAlreadyRegisteredException, EventGivenInvalidStateException, \
    EventMetadata
from tests.tests import ResetDB, TestFilePath

events_db_path = TestFilePath().get_db_path('events.db')
events_db_init_script_path = TestFilePath().get_db_path('events.sql')
test_events = [
    'event_one',
    'event_two'
]

test_event_data = [
    (1, 'event_one', 'REGISTERED'),
    (2, 'event_two', 'REGISTERED')
]

test_event_metadata_list = [
    EventMetadata('event_one', 'REGISTERED'),
    EventMetadata('event_two', 'REGISTERED')
]

ResetDB(db_path=events_db_path, sql_path=events_db_init_script_path)


class TestEventsDBInitialisation:
    def test_initialising_db(self):
        edb = EventsDB(db_path=events_db_path, debug=True)


class TestEventDBRetrieve:
    def test_event_exists(self):
        edb = EventsDB(db_path=events_db_path, debug=True)
        assert edb.event_exists(event_name='event_one') is True
        assert edb.event_exists(event_name='dfjojsfdi') is False

    def test_event_row_to_event_metadata_conversion(self):
        edb = EventsDB(db_path=events_db_path, debug=True)
        metadata = edb.convert_to_event_metadata(event_db_row=test_event_data[0])
        assert isinstance(metadata, EventMetadata)

    def test_get_all_event_names(self):
        edb = EventsDB(db_path=events_db_path, debug=True)
        assert sorted(test_events) == sorted(edb.get_all_event_names())

    def test_get_all_event_data(self):
        edb = EventsDB(db_path=events_db_path, debug=True)
        data = edb.get_data_for_all_events()
        assert test_event_metadata_list[0].get_name() == data[0].get_name()
        assert test_event_metadata_list[1].get_name() == data[1].get_name()
        assert test_event_metadata_list[0].get_state() == data[0].get_state()
        assert test_event_metadata_list[1].get_state() == data[1].get_state()

    def test_get_event_metadata(self):
        edb = EventsDB(db_path=events_db_path, debug=True)
        metadata = edb.get_event_metadata(event_name='event_two')
        assert isinstance(metadata, EventMetadata)

    def test_get_event_state(self):
        edb = EventsDB(db_path=events_db_path, debug=True)
        state = edb.get_event_state(event_name='event_two')
        assert state == EventMetadata.default_state


class TestEventDBCreate:
    def test_register_event_already_registered_throws_exception(self):
        edb = EventsDB(db_path=events_db_path, debug=True)
        with pytest.raises(EventAlreadyRegisteredException):
            edb.register_event(event_name='event_one')

    def test_register_event_successfully_stores_in_db(self):
        edb = EventsDB(db_path=events_db_path, debug=True)
        edb.register_event(event_name='new_event_one')
        assert edb.event_exists(event_name='new_event_one')

    def test_new_events_default_state_is_correct(self):
        edb = EventsDB(db_path=events_db_path, debug=True)
        edb.register_event(event_name='new_event_two')
        metadata = edb.get_event_metadata(event_name='new_event_two')
        assert EventMetadata.default_state == metadata.get_state()

    def test_successful_event_state_change(self):
        edb = EventsDB(db_path=events_db_path, debug=True)
        edb.change_event_state(event_name='event_one', new_state='ONGOING')
        metadata = edb.get_event_metadata(event_name='event_one')
        assert EventMetadata.ongoing_state == metadata.get_state()

    def test_event_state_change_to_nonexistent_throws_exception(self):
        edb = EventsDB(db_path=events_db_path, debug=True)
        with pytest.raises(EventGivenInvalidStateException):
            edb.change_event_state(event_name='event_one', new_state='GARBAGE')
