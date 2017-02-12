import pytest
from charitybot2.persistence.sqlite_repository import SQLiteRepository, InvalidRepositoryException, \
    InvalidRepositoryQueryException
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


test_repository = SQLiteRepository(db_path=':memory:')


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

    def test_executing_valid_sql(self):
        test_repository.open_connection()
        create_query = 'CREATE TABLE `test` (testId INTEGER NOT NULL);'
        test_repository.execute_query(query=create_query, commit=True)
        get_tables_query = 'SELECT name FROM sqlite_master WHERE type="table"'
        cursor_execution = test_repository.execute_query(query=get_tables_query)
        assert 'test' in [table[0] for table in cursor_execution.fetchall()]
        delete_query = 'DROP TABLE `test`'
        test_repository.execute_query(query=delete_query, commit=True)
        cursor_execution = test_repository.execute_query(query=get_tables_query)
        assert 'test' not in [table[0] for table in cursor_execution.fetchall()]
        test_repository.close_connection()

    @pytest.mark.parametrize('query,data,commit', [
        (None, None, None),
        ('', None, None),
        ('', '', None),
        ('', '', False),
        ('SELECT * FROM events;', None, False),
        ('This is not SQL!', (), False)
    ])
    def test_executing_invalid_sql_throws_exception(self, query, data, commit):
        test_repository.open_connection()
        with pytest.raises(InvalidRepositoryQueryException):
            test_repository.execute_query(query=query, data=data, commit=commit)
        test_repository.close_connection()
