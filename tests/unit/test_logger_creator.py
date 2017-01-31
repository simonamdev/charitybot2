from charitybot2.creators.logger_creator import LoggerCreator
from charitybot2.persistence.console_logger import ConsoleLogger
from charitybot2.persistence.repository_logger import RepositoryLogger


class TestLoggerCreatorInstantiation:
    def test_default_debug_is_true(self):
        logger_creator = LoggerCreator()
        assert logger_creator.debug is False


class TestLoggerCreation:
    def test_passing_debug_true_gives_console_logger(self):
        console_logger = LoggerCreator(debug=True).get_logger()
        assert isinstance(console_logger, ConsoleLogger)

    def test_passing_debug_false_gives_repository_logger(self):
        repository_logger = LoggerCreator(debug=False).get_logger()
        assert isinstance(repository_logger, RepositoryLogger)
