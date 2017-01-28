import pytest

from charitybot2.storage.base_db import DatabaseDoesNotExistException, BaseDB
from tests.paths_for_tests import logs_db_path


class TestBaseDBExistence:
    def test_nonexistent_db_throws_exception(self):
        with pytest.raises(DatabaseDoesNotExistException):
            db = BaseDB(file_path='bla/bla/bla', db_name='Nonexistent Test DB', verbose=True)

    def test_existent_db_starts_without_issue(self):
        db = BaseDB(file_path=logs_db_path, db_name='Existent Test DB', verbose=True)
