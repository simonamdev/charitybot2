class InvalidRepositoryException(Exception):
    pass


class BaseRepository:
    def __init__(self, db_path):
        self._db_path = db_path
