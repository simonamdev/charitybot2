from time import sleep

from charitybot2.reporter.purrbot_config import purrbot_config
from charitybot2.reporter.twitch import TwitchAccount, TwitchChatBot
from selenium import webdriver


class TestTwitchChat:
    test_string = 'Charitybot2 automated E2E test string'

    def test_twitch_chat_string_sent_appears(self):
        driver = webdriver.Chrome()
        driver.get('https://www.twitch.tv/purrcat259')
        assert 'Purrcat259 - Twitch' == driver.title
        bot_account = TwitchAccount(twitch_config=purrbot_config)
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

