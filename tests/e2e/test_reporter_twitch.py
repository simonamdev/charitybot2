import pytest

from selenium import webdriver

from charitybot2.reporter.twitch import TwitchAccount, InvalidTwitchAccountException, TwitchChatBot
from charitybot2.reporter.twitch_config import client_id, client_secret


class TestTwitchAccount:
    def test_invalid_twitch_account_throws_exception(self):
        with pytest.raises(InvalidTwitchAccountException):
            TwitchAccount(name='osdfjoidsfjiuosdfjiosfdjio', client_id=client_id, client_secret='bla')

    def test_twitch_account_exists(self):
        purrcat = TwitchAccount(name='purrcat259', client_id=client_id, client_secret='bla')


class TestTwitchChat:
    driver = webdriver.Chrome()
    test_string = 'Hello, I am an automated E2E Test!'

    def test_twitch_chat_string_sent_appears(self):
        self.driver.get('https://www.twitch.tv/purrcat259')
        assert 'Purrcat259 - Twitch' == self.driver.title
        bot_account = TwitchAccount(name='purrcat259', client_id=client_id, client_secret=client_secret)
        bot = TwitchChatBot(
            channel_name='purrcat259',
            twitch_account=bot_account,
            verbose=True
        )
        bot.post_in_channel(self.test_string)
        chat_window = self.driver.find_element_by_class_name('chat-display')
        print(chat_window.text)
        assert self.test_string in chat_window.text
        self.driver.close()
