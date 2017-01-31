import pytest
from charitybot2.persistence.sqlite_repository import SQLiteRepository, InvalidRepositoryException
from tests.paths_for_tests import test_repository_db_path, valid_event_config_path


class TestSQLiteRepositoryInstantiation:
    def test_default_debug_is_false(self):
        base_repository = SQLiteRepository(db_path=test_repository_db_path)
        assert base_repository.debug is False


class TestSQLiteRepositoryExceptions:
    @pytest.mark.parametrize('db_path', [
        None,
        123,
        valid_event_config_path,
        '',
        'Bla'
    ])
    def test_passing_invalid_path_throws_exception(self, db_path):
        with pytest.raises(InvalidRepositoryException):
            SQLiteRepository(db_path=db_path)

    def test_passing_incorrect_db_paths_throws_exception(self):
        with pytest.raises(FileNotFoundError):
            SQLiteRepository(db_path='bla/bla.db')


test_repository = SQLiteRepository(db_path=test_repository_db_path)


class TestSQLiteRepositoryConnections:
    def test_opening_connection(self):
        test_repository.open_connection()
        assert True is test_repository.connection_open

    def test_closing_connection(self):
        test_repository.open_connection()
        test_repository.close_connection()
        assert False is test_repository.connection_open

    def test_closing_connection_after_not_opening(self):
        test_repository.close_connection()
        assert False is test_repository.connection_open