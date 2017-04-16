import os


class SQLScript:
    def __init__(self, path):
        self._path = path
        self.__validate_file()

    def __validate_file(self):
        if not os.path.isfile(self.path):
            pass

    def __read_file(self):
        pass

    def return_sql(self):
        pass

    @property
    def path(self):
        return self._path
