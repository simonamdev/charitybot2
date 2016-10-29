import pytest
from charitybot2.storage.db_handler import DBCouldNotBeFoundException, DBHandler
from charitybot2.storage.donations_db import DonationsDB
from tests.tests import TestFilePath

test_donations_db_path = TestFilePath().get_db_path('donations.db')


class TestDBHandlerValidity:
    def test_initialising_with_invalid_path_throws_exception(self):
        with pytest.raises(DBCouldNotBeFoundException):
            dbh = DBHandler(donations_db_path='', debug=True)

    def test_passing_valid_paths_starts_normally(self):
        dbh = DBHandler(donations_db_path=test_donations_db_path, debug=True)

    def test_returning_db_connections_are_of_expected_types(self):
        dbh = DBHandler(donations_db_path=test_donations_db_path, debug=True)
        assert isinstance(dbh.get_donations_db(), DonationsDB)
