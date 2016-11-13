import time

import requests
from bs4 import BeautifulSoup
from charitybot2.charitybot2 import CharityBot, create_parser
from charitybot2.events.currency import Currency
from charitybot2.paths import mocksite_path, external_api_path
from charitybot2.reporter.external_api.external_api import api_full_url
from charitybot2.reporter.twitch import ChatBot
from selenium import webdriver
from tests.integration.test_event_loop_with_mocksite import MockEvent
from tests.tests import ServiceTest, AdjustTestConfig, TestFilePath

driver = None
parser = create_parser()
config_adjustment = AdjustTestConfig(config_path=TestFilePath().get_config_path('event', 'config.json'))
service_test = ServiceTest(
    service_name='Donations Mocksite',
    service_url=MockEvent.mocksite_base_url,
    service_path=mocksite_path,
    enter_debug=False)

external_api = ServiceTest(
    service_name='External_API',
    service_url=api_full_url,
    service_path=external_api_path,
    enter_debug=True)


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
    external_api.start_service()
    global driver
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)


def teardown_module():
    service_test.stop_service()
    external_api.stop_service()
    global driver
    driver.close()


class TestFullTwitchEvent:
    def test_full_twitch_event(self):
        config_adjustment.change_value(key='end_time', value=int(time.time()) + 20)
        navigate_to_twitch_channel()
        args = parser.parse_args(['config', '--debug', '--twitch-config', 'purrcat259'])
        bot = CharityBot(args=args)
        bot.initialise_bot()
        bot.start_bot()
        time.sleep(4)
        expected_string = 'Purrcat259 : ' + ChatBot.donation_string.format(Currency.GBP, 200.52, Currency.GBP, 200.52)
        expected_string_two = 'Purrcat259 : ' + ChatBot.donation_string.format(Currency.GBP, 50.0, Currency.GBP, 250.52)
        chat_box_contents = get_twitch_chat_box_contents()
        assert expected_string in chat_box_contents
        assert expected_string_two in chat_box_contents


class TestFullAPIEvent:
    def test_full_event(self):
        config_adjustment.change_value(key='end_time', value=int(time.time()) + 10)
        args = parser.parse_args(['config', '--debug'])
        bot = CharityBot(args=args)
        bot.initialise_bot()
        bot.start_bot()
        response = requests.get(url=api_full_url + 'event/E2E_Test_Charity_Event/overlay')
        assert 200 == response.status_code
        assert '<!DOCTYPE html>' in response.content.decode('utf-8')
        soup = BeautifulSoup(response.content, 'html.parser')
        amount_raised = soup.find('span', {'id': 'amount_raised'}).text.strip()
        assert '£250.52' == amount_raised
