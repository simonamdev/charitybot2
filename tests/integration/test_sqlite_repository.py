import pytest
from charitybot2.paths import valid_test_event_config_path
from charitybot2.persistence.sqlite_repository import SQLiteRepository, InvalidRepositoryException, \
    InvalidRepositoryQueryException


class TestSQLiteRepositoryExceptions:
    @pytest.mark.parametrize('db_path', [
        None,
        123,
        valid_test_event_config_path
    ])
    def test_passing_invalid_path_throws_exception(self, db_path):
        with pytest.raises(InvalidRepositoryException):
            SQLiteRepository(db_path=db_path)

    def test_passing_incorrect_db_paths_throws_exception(self):
        with pytest.raises(FileNotFoundError):
            SQLiteRepository(db_path='bla/bla.db')


class TestSQLiteRepository:
    test_repository = None

    def setup_method(self):
        self.test_repository = SQLiteRepository(db_path='memory')

    def teardown_method(self):
        self.test_repository.close_connection()

    def test_opening_connection(self):
        assert True is self.test_repository.connection_open

    def test_closing_connection(self):
        self.test_repository.close_connection()
        assert False is self.test_repository.connection_open

    def test_executing_valid_sql(self):
        create_query = 'CREATE TABLE `test` (testId INTEGER NOT NULL);'
        self.test_repository.execute_query(query=create_query, commit=True)
        get_tables_query = 'SELECT name FROM sqlite_master WHERE type="table"'
        cursor_execution = self.test_repository.execute_query(query=get_tables_query)
        assert 'test' in [table[0] for table in cursor_execution.fetchall()]
        delete_query = 'DROP TABLE `test`'
        self.test_repository.execute_query(query=delete_query, commit=True)
        cursor_execution = self.test_repository.execute_query(query=get_tables_query)
        assert 'test' not in [table[0] for table in cursor_execution.fetchall()]
        self.test_repository.close_connection()

    @pytest.mark.parametrize('query,data,commit', [
        (None, None, None),
        ('', None, None),
        ('', '', None),
        ('', '', False),
        ('SELECT * FROM events;', None, False),
        ('This is not SQL!', (), False)
    ])
    def test_executing_invalid_sql_throws_exception(self, query, data, commit):
        with pytest.raises(InvalidRepositoryQueryException):
            self.test_repository.execute_query(query=query, data=data, commit=commit)
            self.test_repository.close_connection()
