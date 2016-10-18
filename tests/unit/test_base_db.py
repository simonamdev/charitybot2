import os

import pytest

from charitybot2.storage.base_db import DatabaseDoesNotExistException, BaseDB


current_directory = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_directory, 'db', 'test_events.db')


class TestBaseDBExistence:
    def test_nonexistent_db_throws_exception(self):
        with pytest.raises(DatabaseDoesNotExistException):
            db = BaseDB(file_path='bla/bla/bla', db_name='Nonexistent Test DB', verbose=True)

    def test_existent_db_starts_without_issue(self):
        db = BaseDB(file_path=db_path, db_name='Existent Test DB', verbose=True)
