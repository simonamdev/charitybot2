from charitybot2.paths import production_repository_db_path
from charitybot2.persistence.sqlite_repository import SQLiteRepository
from tests.paths_for_tests import test_repository_db_path


class EventNotRegisteredException(Exception):
    pass


class EventRepository(SQLiteRepository):
    def __init__(self, debug=False):
        self._db_path = production_repository_db_path if not debug else test_repository_db_path
        super().__init__(db_path=self._db_path)

    @property
    def db_path(self):
        return self._db_path

    def get_event(self, identifier):
        pass
