from charitybot2.models.log import LogLevel
from charitybot2.paths import production_logs_db_path
from charitybot2.persistence.repository_logger import RepositoryLogger
from tests.mocks import WipeSQLiteDB

sqlite_db_wipe = WipeSQLiteDB(db_path=production_logs_db_path)


class TestRepositoryLogger:
    def test_get_all_logs(self):
        sqlite_db_wipe.wipe_db()
        test_repository_logger = RepositoryLogger(source='test_source', event='test_event')
        test_repository_logger.log_verbose(timestamp=1, message='all log test')
        test_repository_logger.log_info(timestamp=1, message='all log test')
        test_repository_logger.log_warning(timestamp=1, message='all log test')
        test_repository_logger.log_error(timestamp=1, message='all log test')
        all_logs = test_repository_logger.get_all_logs()
        assert 4 == len(all_logs)
        for log in all_logs:
            assert 'all log test' == log.message
            assert 1 == log.timestamp
            assert 'test_source' == log.source
            assert 'test_event' == log.event

    def test_getting_specific_logs_without_params_returns_all_logs(self):
        sqlite_db_wipe.wipe_db()
        test_repository_logger = RepositoryLogger(source='test_source', event='test_event')
        test_repository_logger.log_verbose(timestamp=1, message='no params test')
        test_repository_logger.log_info(timestamp=1, message='no params test')
        all_logs = test_repository_logger.get_specific_logs()
        assert 2 == len(all_logs)
        for log in all_logs:
            assert 'no params test' == log.message
            assert 1 == log.timestamp
            assert 'test_source' == log.source
            assert 'test_event' == log.event

    def test_getting_logs_by_single_timestamp(self):
        sqlite_db_wipe.wipe_db()
        test_repository_logger = RepositoryLogger(source='test_source', event='test_event')
        test_repository_logger.log_verbose(timestamp=2, message='one timestamp test')
        test_repository_logger.log_info(timestamp=3, message='one timestamp test')
        timestamp_logs = test_repository_logger.get_specific_logs(timestamp=2)
        assert 1 == len(timestamp_logs)
        assert 2 == timestamp_logs[0].timestamp
        assert 'one timestamp test' == timestamp_logs[0].message
        assert 'test_source' == timestamp_logs[0].source
        assert 'test_event' == timestamp_logs[0].event

    def test_getting_logs_by_timestamp_range(self):
        sqlite_db_wipe.wipe_db()
        test_repository_logger = RepositoryLogger(source='test_source', event='test_event')
        test_repository_logger.log_verbose(timestamp=4, message='timestamp test')
        test_repository_logger.log_info(timestamp=5, message='timestamp test')
        test_repository_logger.log_warning(timestamp=6, message='timestamp test')
        test_repository_logger.log_error(timestamp=7, message='timestamp test')
        timestamp_logs = test_repository_logger.get_specific_logs(timestamp=(4, 7))
        assert 4 == len(timestamp_logs)
        for log in timestamp_logs:
            assert 'timestamp test' == log.message

    def test_getting_logs_by_level(self):
        sqlite_db_wipe.wipe_db()
        test_repository_logger = RepositoryLogger(source='test_source', event='test_event')
        test_repository_logger.log_verbose(timestamp=10, message='verbose')
        test_repository_logger.log_verbose(timestamp=10, message='verbose')
        test_repository_logger.log_verbose(timestamp=10, message='verbose')
        test_repository_logger.log_info(timestamp=10, message='info')
        info_logs = test_repository_logger.get_specific_logs(level=LogLevel.info)
        assert 1 == len(info_logs)
        assert 'info' == info_logs.message
        error_logs = test_repository_logger.get_specific_logs(level=LogLevel.error)
        assert 0 == len(error_logs)

    def test_getting_logs_by_event(self):
        sqlite_db_wipe.wipe_db()
        test_repository_logger = RepositoryLogger(source='test_source', event='test_event')
        test_repository_logger.log_verbose(timestamp=1, message='event')
        test_repository_logger.log_info(timestamp=1, message='event')
        test_repository_logger.log_warning(timestamp=1, message='event')
        event_logs = test_repository_logger.get_specific_logs(event='test_event')
        assert 3 == len(event_logs)
        for log in event_logs:
            assert 'test_event' == log.message
        non_existent_event_logs = test_repository_logger.get_specific_logs(event='blabla')
        assert 0 == len(non_existent_event_logs)

    def test_getting_logs_by_source(self):
        sqlite_db_wipe.wipe_db()
        test_repository_logger = RepositoryLogger(source='test_source', event='test_event')
        test_repository_logger.log_verbose(timestamp=1, message='source')
        test_repository_logger.log_info(timestamp=1, message='source')
        test_repository_logger.log_warning(timestamp=1, message='source')
        test_repository_logger.log_error(timestamp=1, message='source')
        test_repository_logger.log_info(timestamp=1, message='source')
        source_logs = test_repository_logger.get_specific_logs(source='test_source')
        assert 5 == len(source_logs)
        for log in source_logs:
            assert 'test_source' == log.message
        non_existent_source_logs = test_repository_logger.get_specific_logs(source='foobar')
        assert 0 == len(non_existent_source_logs)
