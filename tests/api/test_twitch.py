import pytest
from charitybot2.botconfig.twitch_config import TwitchAccountConfiguration
from charitybot2.reporter.purrbot_config import purrbot_config
from charitybot2.reporter.twitch import InvalidTwitchAccountException, TwitchAccount
from tests.restters_for_tests import TestFilePath

invalid_config_path = TestFilePath().get_config_path('twitch', 'test_twitch_config.json')


class TestTwitchAccount:
    def test_invalid_twitch_account_throws_exception(self):
        with pytest.raises(InvalidTwitchAccountException):
            invalid_config = TwitchAccountConfiguration(file_path=invalid_config_path)
            TwitchAccount(twitch_config=invalid_config)

    def test_twitch_account_exists(self):
        purrbot = TwitchAccount(twitch_config=purrbot_config)
        purrbot.validate_twitch_account()
