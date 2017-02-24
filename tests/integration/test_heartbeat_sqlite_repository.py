from charitybot2.persistence.heartbeat_sqlite_repository import HeartbeatSQLiteRepository
from tests.paths_for_tests import test_repository_db_path


class TestHeartbeatSQLiteRepositoryInstantiation:
    def test_default_debug_is_false(self):
        heartbeat_repository = HeartbeatSQLiteRepository(
            db_path=test_repository_db_path)
        assert heartbeat_repository.debug is False


class TestHeartbeatSQLiteRepository:
    pass


class TestHeartbeatSQLiteRepositoryExceptions:
    pass
