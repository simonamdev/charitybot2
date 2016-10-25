import os

import pytest
from charitybot2.storage.db_handler import DBCouldNotBeFoundException, DBHandler
from charitybot2.storage.donations_db import DonationsDB
from charitybot2.storage.events_db import EventsDB

current_directory = os.path.dirname(os.path.abspath(__file__))
test_event_db_path = os.path.join(current_directory, 'db', 'test_events.db')
test_donations_db_path = os.path.join(current_directory, 'db', 'test_donations.db')


class TestDBHandlerValidity:
    def test_initialising_with_both_invalid_paths_throws_exception(self):
        with pytest.raises(DBCouldNotBeFoundException):
            dbh = DBHandler(events_db_path='', donations_db_path='', debug=True)

    def test_initialising_with_one_invalid_path_throws_exception(self):
        with pytest.raises(DBCouldNotBeFoundException):
            dbh = DBHandler(events_db_path=test_event_db_path, donations_db_path='', debug=True)

    def test_initialising_with_other_invalid_path_throws_exception(self):
        with pytest.raises(DBCouldNotBeFoundException):
            dbh = DBHandler(events_db_path='', donations_db_path=test_donations_db_path, debug=True)

    def test_passing_valid_paths_starts_normally(self):
        dbh = DBHandler(events_db_path=test_event_db_path, donations_db_path=test_donations_db_path, debug=True)

    def test_returning_db_connections_is_of_expected_types(self):
        dbh = DBHandler(events_db_path=test_event_db_path, donations_db_path=test_donations_db_path, debug=True)
        assert isinstance(dbh.get_events_db(), EventsDB)
        assert isinstance(dbh.get_donations_db(), DonationsDB)
