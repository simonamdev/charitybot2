import pytest
from charitybot2.charitybot2 import MissingRequiredFileException
from charitybot2.start_bot import Startup, create_parser, IllegalArgumentException


class TestParserRequiredArguments:
    parser = create_parser()

    def test_passing_empty_event_name_throws_exception(self):
        args = self.parser.parse_args(['', '--debug'])
        with pytest.raises(IllegalArgumentException):
            Startup(args=args)

    def test_passing_non_existent_event_config_throws_exception(self):
        args = self.parser.parse_args(['test', '--debug'])
        with pytest.raises(MissingRequiredFileException):
            Startup(args=args)

    def test_passing_existent_event_config(self):
        args = self.parser.parse_args(['config', '--debug'])
        Startup(args=args)


class TestParserOptionalArguments:
    parser = create_parser()

    def test_passing_non_existent_twitch_config_in_twitch_mode_throws_exception(self):
        args = self.parser.parse_args(['config', '--debug', '--twitch-config', 'bla'])
        with pytest.raises(MissingRequiredFileException):
            Startup(args=args)

    def test_passing_existent_twitch_config_in_twitch_mode(self):
        args = self.parser.parse_args(['config', '--debug', '--twitch-config', 'test_twitch_config'])
        Startup(args=args)
