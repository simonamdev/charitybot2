import time
from charitybot2.charitybot2 import CharityBot, create_parser
from charitybot2.events.currency import Currency
from charitybot2.paths import mocksite_path
from charitybot2.reporter.twitch import ChatBot
from selenium import webdriver
from tests.integration.test_event_loop_with_mocksite import MockEvent
from tests.tests import ServiceTest

driver = None
parser = create_parser()
service_test = ServiceTest(
    service_name='Donations Mocksite',
    service_url=MockEvent.mocksite_base_url,
    service_path=mocksite_path,
    enter_debug=False)


# Duplicated from other E2E test, could do with a common refactor
def navigate_to_twitch_channel():
    global driver
    driver.get('https://www.twitch.tv/purrcat259')
    assert 'Purrcat259 - Twitch' == driver.title
    time.sleep(2)


def get_twitch_chat_box_contents():
    return driver.find_element_by_class_name('chat-display').text


def setup_module():
    service_test.start_service()
    global driver
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)


def teardown_module():
    service_test.stop_service()
    global driver
    driver.close()


class TestFullTwitchEvent:
    def test_full_twitch_event(self):
        navigate_to_twitch_channel()
        args = parser.parse_args(['config', '--debug', '--twitch-config', 'purrcat259'])
        bot = CharityBot(args=args)
        bot.initialise_bot()
        bot.start_bot()
        time.sleep(4)
        expected_string = ChatBot.donation_string.format(Currency.GBP, 35517.0, Currency.GBP, 35517.0)
        assert expected_string in get_twitch_chat_box_contents()


class TestFullAPIEvent:
    pass
