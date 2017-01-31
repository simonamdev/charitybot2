import os

import sqlite3


class InvalidRepositoryException(Exception):
    pass


class SQLiteRepository:
    def __init__(self, db_path, debug=False):
        self._db_path = db_path
        self._debug = debug
        self._connection = None
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
        if '.db' not in self._db_path and '.sqlite' not in self._db_path:
            raise InvalidRepositoryException('Given path does not lead to a valid database file')
        if not os.path.isfile(self._db_path):
            raise FileNotFoundError('Database file not found at given DB Path')

    def open_connection(self):
        self._connection = sqlite3.connect(database=self._db_path)

    def close_connection(self):
        if self._connection is not None:
            self._connection.close()
        self._connection = None
