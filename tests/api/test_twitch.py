import pytest
from charitybot2.reporter.purrbot_config import purrbot_config
from charitybot2.reporter.twitch import InvalidTwitchAccountException, TwitchAccount


class TestTwitchAccount:
    def test_invalid_twitch_account_throws_exception(self):
        with pytest.raises(InvalidTwitchAccountException):
            TwitchAccount(name='osdfjoidsfjiuosdfjiosfdjio', twitch_config=purrbot_config)

    def test_twitch_account_exists(self):
        purrcat = TwitchAccount(name='purrcat259', twitch_config=purrbot_config)
        purrcat.validate_twitch_account()
