import pytest
from charitybot2.models.log import LogLevel
from charitybot2.persistence.logger import Logger


class MockLogger(Logger):
    def log(self, log):
        return log


test_mock_logger = MockLogger(source='test_source', event='test_event')


class TestLogger:
    @pytest.mark.parametrize('expected,actual', [
        (test_mock_logger.log_verbose(timestamp=1, message='test').timestamp, 1),
        (test_mock_logger.log_verbose(timestamp=1, message='test').message, 'test'),
        (test_mock_logger.log_verbose(timestamp=1, message='test').level, LogLevel.verbose)
    ])
    def test_retrieval_of_verbose(self, expected, actual):
        assert expected == actual

    @pytest.mark.parametrize('expected,actual', [
        (test_mock_logger.log_info(timestamp=1, message='test').timestamp, 1),
        (test_mock_logger.log_info(timestamp=1, message='test').message, 'test'),
        (test_mock_logger.log_info(timestamp=1, message='test').level, LogLevel.info)
    ])
    def test_retrieval_of_info(self, expected, actual):
        assert expected == actual

    @pytest.mark.parametrize('expected,actual', [
        (test_mock_logger.log_warning(timestamp=1, message='test').timestamp, 1),
        (test_mock_logger.log_warning(timestamp=1, message='test').message, 'test'),
        (test_mock_logger.log_warning(timestamp=1, message='test').level, LogLevel.warning)
    ])
    def test_retrieval_of_warning(self, expected, actual):
        assert expected == actual

    @pytest.mark.parametrize('expected,actual', [
        (test_mock_logger.log_error(timestamp=1, message='test').timestamp, 1),
        (test_mock_logger.log_error(timestamp=1, message='test').message, 'test'),
        (test_mock_logger.log_error(timestamp=1, message='test').level, LogLevel.error)
    ])
    def test_retrieval_of_error(self, expected, actual):
        assert expected == actual
