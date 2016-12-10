from neopysqlite import neopysqlite


class DatabaseDoesNotExistException(Exception):
    pass


class BaseDB:
    def __init__(self, file_path, db_name, verbose=False):
        self.db_path = file_path
        self.db_name = db_name
        self.verbose = verbose
        self.db = None
        self.initialise()

    def initialise(self):
        try:
            self.db = neopysqlite.Neopysqlite(database_name=self.db_name, db_path=self.db_path, verbose=self.verbose)
        except Exception:
            raise DatabaseDoesNotExistException('Database {} could not be found at path: {}'.format(
                self.db_name,
                self.db_path))
