import os

import sqlite3


class InvalidRepositoryException(Exception):
    pass


class InvalidRepositoryQueryException(Exception):
    pass


class InvalidDatabasePathException(Exception):
    pass


class SQLiteRepository:
    def __init__(self, db_path, debug=False):
        self._db_path = db_path
        self._debug = debug
        self._connection = None
        self._cursor = None
        self.__validate_database()

    @property
    def debug(self):
        return self._debug

    @property
    def connection_open(self):
        return self._connection is not None

    def __validate_database(self):
        if not isinstance(self._db_path, str):
            raise InvalidRepositoryException('Given path is not a string')
        if '.db' not in self._db_path and '.sqlite' not in self._db_path and not self._db_path == ':memory:':
            raise InvalidRepositoryException('Given path does not lead to a valid database file')
        if not os.path.isfile(self._db_path) and not self._db_path == ':memory:':
            raise FileNotFoundError('Database file not found at given DB Path')

    def open_connection(self):
        self._connection = sqlite3.connect(database=self._db_path)
        self._cursor = self._connection.cursor()

    def close_connection(self):
        if self._connection is not None:
            self._cursor.close()
            self._connection.close()
        self._cursor = None
        self._connection = None

    def execute_query(self, query, data=(), commit=False):
        self.__validate_query_parameters(query=query, data=data, commit=commit)
        try:
            if commit:
                self._cursor.execute(query, data)
                self._connection.commit()
            else:
                return self._cursor.execute(query, data)
        except sqlite3.OperationalError as e:
            raise InvalidRepositoryQueryException(str(e))

    @staticmethod
    def __validate_query_parameters(query, data, commit):
        if None in (query, data, commit):
            raise InvalidRepositoryQueryException('Cannot pass null values to query')
        if query == '':
            raise InvalidRepositoryQueryException('Query cannot be empty')
