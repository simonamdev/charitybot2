from time import sleep
from selenium import webdriver

from charitybot2.reporter.twitch import TwitchAccount, TwitchChatBot
from charitybot2.reporter.twitch_config import client_id, client_secret


class TestTwitchChat:
    test_string = 'Charitybot2 automated E2E test string'

    def test_twitch_chat_string_sent_appears(self):
        driver = webdriver.Chrome()
        driver.get('https://www.twitch.tv/purrcat259')
        assert 'Purrcat259 - Twitch' == driver.title
        bot_account = TwitchAccount(name='purrcat259', client_id=client_id, client_secret=client_secret)
        bot = TwitchChatBot(
            channel_name='purrcat259',
            twitch_account=bot_account,
            verbose=True
        )
        bot.quick_post_in_channel(self.test_string)
        sleep(4)
        chat_window = driver.find_element_by_class_name('chat-display')
        print(chat_window.text)
        assert self.test_string in chat_window.text
        driver.close()

