import os

from type_assertions import accept_types


class SQLScript:
    def __init__(self, path):
        self._path = path
        self._raw_sql = ''
        self.__validate_file(path)
        self.__read_file()

    @accept_types(object, str)
    def __validate_file(self, path):
        if not os.path.isfile(path):
            raise FileNotFoundError('SQL Script not present at path: {}'.format(path))

    def __read_file(self):
        with open(self._path, 'r') as sql_file:
            lines = sql_file.readlines()
            for line in lines:
                self._raw_sql += line.strip()

    def return_sql(self):
        return self._raw_sql

    @property
    def path(self):
        return self._path
