import pytest
from charitybot2.persistence.heartbeat_sqlite_repository import HeartbeatSQLiteRepository, NonExistentHeartbeat


heartbeat_repository = HeartbeatSQLiteRepository(debug=True)
heartbeat_repository.store_heartbeat(source='test_source', state='test_state', timestamp=1)


def teardown_module():
    heartbeat_repository.close_connection()


class TestHeartbeatSQLiteRepository:
    def test_retrieving_last_heartbeat(self):
        last_heartbeat = heartbeat_repository.get_last_heartbeat(source='test_source')
        assert 'test_source' == last_heartbeat['source']
        assert 'test_state' == last_heartbeat['state']
        assert 1 == last_heartbeat['timestamp']

    def test_insert_heartbeat_state(self):
        heartbeat_repository.store_heartbeat(source='test_insert_source', state='test_insert_state', timestamp=2)
        new_heartbeat = heartbeat_repository.get_last_heartbeat(source='test_insert_source')
        assert 'test_insert_source' == new_heartbeat['source']
        assert 'test_insert_state' == new_heartbeat['state']
        assert 2 == new_heartbeat['timestamp']


class TestHeartbeatSQLiteRepositoryExceptions:
    def test_retrieving_from_non_existent_source_throws_exception(self):
        with pytest.raises(NonExistentHeartbeat):
            nonexistent_source_heartbeat = heartbeat_repository.get_last_heartbeat(source='non-existent')
