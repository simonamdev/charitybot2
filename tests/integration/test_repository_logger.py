import pytest
from charitybot2.persistence.repository_logger import RepositoryLogger

test_repository_logger = RepositoryLogger(source='test_source', event='test_event')


class TestRepositoryLogger:
    def test_get_all_logs(self):
        test_repository_logger.log_verbose(timestamp=1, message='all log test')
        test_repository_logger.log_info(timestamp=1, message='all log test')
        test_repository_logger.log_warning(timestamp=1, message='all log test')
        test_repository_logger.log_error(timestamp=1, message='all log test')
        all_logs = test_repository_logger.get_all_logs()
        assert 4 == len(all_logs)
        for log in all_logs:
            assert 'all log test' == log.message
            assert 1 == log.timestamp

    def test_getting_logs_by_timestamp(self):
        test_repository_logger.log_verbose(timestamp=2, message='timestamp test')
        test_repository_logger.log_info(timestamp=3, message='timestamp test')
        test_repository_logger.log_warning(timestamp=4, message='timestamp test')
        test_repository_logger.log_error(timestamp=5, message='timestamp test')

    def test_getting_logs_by_level(self):
        assert False is True

    def test_getting_logs_by_event(self):
        assert False is True


class TestRepositoryLoggerExceptions:
    @pytest.mark.parametrize('log', [

    ])
    def test_passing_invalid_logs_throw_exceptions(self, log):
        pass
