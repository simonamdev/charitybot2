from charitybot2.storage.logger import Logger


class MockLogger(Logger):


class TestLoggerValidity:
    def test_logger_with_bad_url_throws_exception(self):
