import uuid
import time

import pytest
from charitybot2.events.event_loop import TwitchEventLoop
from charitybot2.events.currency import Currency
from charitybot2.paths import mocksite_path
from charitybot2.reporter.purrbot_config import purrbot_config
from charitybot2.reporter.twitch import TwitchAccount, TwitchChatBot, ChatBot
from selenium import webdriver
from tests.integration.test_event_loop_with_mocksite import MockEvent
from tests.paths_for_tests import end_to_end_config_path
from tests.restters_for_tests import ServiceTest


def return_unique_test_string():
    base_string = 'Charitybot2 automated E2E test string [{}]'
    return base_string.format(str(uuid.uuid4()))

driver = None
purrbot = TwitchAccount(twitch_config=purrbot_config)
service_test = ServiceTest(
    service_name='Donations Mocksite',
    service_url=MockEvent.mocksite_base_url,
    service_path=mocksite_path,
    enter_debug=False)


def setup_module():
    service_test.start_service()
    global driver
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)


def teardown_module():
    service_test.stop_service()
    global driver
    driver.close()


def get_twitch_chat_box_contents():
    return driver.find_element_by_class_name('chat-display').text


def navigate_to_twitch_channel():
    global driver
    driver.get('https://www.twitch.tv/purrcat259')
    assert 'Purrcat259 - Twitch' == driver.title
    time.sleep(2)


class TestTwitchChat:
    def test_twitch_chat_string_sent_appears(self):
        navigate_to_twitch_channel()
        test_string = return_unique_test_string()
        bot = TwitchChatBot(
            channel_name='purrcat259',
            twitch_account=purrbot,
            verbose=True)
        bot.quick_post_in_channel(test_string)
        time.sleep(4)
        assert test_string in get_twitch_chat_box_contents()

    @pytest.mark.skip(reason='Currently out of scope')
    def test_twitch_chat_donations_appear(self):
        navigate_to_twitch_channel()
        test_event = MockEvent(end_to_end_config_path, 'e2e_twitch_event', int(time.time()) + 20)
        test_event_loop = TwitchEventLoop(event=test_event, twitch_account=purrbot, debug=True)
        test_event_loop.start()
        time.sleep(4)
        expected_string = ChatBot.donation_string.format(Currency.GBP, 250.52, Currency.GBP, 250.52)
        assert expected_string in get_twitch_chat_box_contents()
