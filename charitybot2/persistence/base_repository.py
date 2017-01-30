import os


class InvalidRepositoryException(Exception):
    pass


class BaseRepository:
    def __init__(self, db_path, debug=False):
        self._db_path = db_path
        self._debug = debug
        self.__validate_database()

    @property
    def debug(self):
        return self._debug

    def __validate_database(self):
        if not isinstance(self._db_path, str):
            raise InvalidRepositoryException('Given path is not a string')
        if '.db' not in self._db_path and '.sqlite' not in self._db_path:
            raise InvalidRepositoryException('Given path does not lead to a valid database file')
        if not os.path.isfile(self._db_path):
            raise FileNotFoundError('Database file not found at given DB Path')
