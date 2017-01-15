import pytest

from charitybot2.storage.base_db import DatabaseDoesNotExistException, BaseDB
from tests.test_helpers import TestFilePath

db_path = TestFilePath().get_db_path('logs.db')


class TestBaseDBExistence:
    def test_nonexistent_db_throws_exception(self):
        with pytest.raises(DatabaseDoesNotExistException):
            db = BaseDB(file_path='bla/bla/bla', db_name='Nonexistent Test DB', verbose=True)

    def test_existent_db_starts_without_issue(self):
        db = BaseDB(file_path=db_path, db_name='Existent Test DB', verbose=True)
