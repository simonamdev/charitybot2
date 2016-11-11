import pytest
from charitybot2.charitybot2 import MissingRequiredFileException
from charitybot2.start_bot import Startup, create_parser, IllegalArgumentException


class TestParserRequiredArguments:
    def test_passing_empty_event_name_throws_exception(self):
        parser = create_parser()
        args = parser.parse_args(['', '--debug'])
        with pytest.raises(IllegalArgumentException):
            Startup(args=args)

    def test_passing_non_existent_event_configs_throws_exception(self):
        parser = create_parser()
        args = parser.parse_args(['test', '--debug'])
        with pytest.raises(MissingRequiredFileException):
            Startup(args=args)
