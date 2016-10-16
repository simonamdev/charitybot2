import pytest

from selenium import webdriver

from charitybot2.reporter.twitch import TwitchAccount, InvalidTwitchAccountException
from charitybot2.reporter.twitch_config import client_id


class TestTwitchAccount:
    def test_invalid_twitch_account_throws_exception(self):
        with pytest.raises(InvalidTwitchAccountException):
            TwitchAccount(name='osdfjoidsfjiuosdfjiosfdjio', token=client_id)

    def test_twitch_account_exists(self):
        purrcat = TwitchAccount(name='purrcat259', token=client_id)


class TestTwitchChat:
    driver = webdriver.Chrome()

    def test_twitch_chat_string_sent_appears(self):
        self.driver.get('https://www.twitch.tv/purrcat259')
        assert 'Purrcat259 - Twitch' == self.driver.title
        self.driver.close()
