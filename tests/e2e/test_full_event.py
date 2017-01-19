import time

import pytest
import requests
from bs4 import BeautifulSoup
from charitybot2.botconfig.event_config import EventConfigurationFromFile
from charitybot2.charitybot2 import CharityBot, create_cb_process_parser
from charitybot2.events.currency import Currency
from charitybot2.paths import mocksite_path, external_api_cli_path
from charitybot2.reporter.external_api.external_api import api_full_url
from charitybot2.reporter.twitch import ChatBot
from selenium import webdriver
from tests.e2e.test_reporter_twitch import navigate_to_twitch_channel, get_twitch_chat_box_contents
from tests.integration.test_event_loop_with_mocksite import MockEvent
from tests.paths_for_tests import end_to_end_config_path, repository_db_path, repository_db_script_path
from tests.mocks import ServiceTest, AdjustTestConfig, ResetDB

driver = None
parser = create_cb_process_parser()
config_adjustment = AdjustTestConfig(config_path=end_to_end_config_path)
event_config = EventConfigurationFromFile(file_path=end_to_end_config_path).get_event_configuration()

service_test = ServiceTest(
    service_name='Donations Mocksite',
    service_url=MockEvent.mocksite_base_url,
    service_path=mocksite_path,
    enter_debug=False)

external_api = ServiceTest(
    service_name='External API',
    service_url=api_full_url,
    service_path=external_api_cli_path,
    extra_args=['--debug'],
    enter_debug=True)


def setup_module():
    service_test.start_service()
    external_api.start_service()
    global driver
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)


def teardown_module():
    service_test.stop_service()
    external_api.stop_service()
    global driver
    driver.close()


class TestFullTwitchEvent:
    @pytest.mark.skip(reason='Currently out of scope')
    def test_full_twitch_event(self):
        ResetDB(db_path=repository_db_path, sql_path=repository_db_script_path)
        config_adjustment.change_value(key='end_time', value=int(time.time()) + 30)
        navigate_to_twitch_channel()
        args = parser.parse_args(['e2e_config', '--debug', '--twitch-config', 'purrcat259'])
        bot = CharityBot(args=args)
        bot.initialise_bot()
        bot.start_bot()
        expected_string = 'Purrcat259 : ' + ChatBot.donation_string.format(Currency.GBP, 100.52, Currency.GBP, 100.52)
        chat_box_contents = get_twitch_chat_box_contents()
        assert expected_string in chat_box_contents
        # rerun to change amount and test that the value already in the database is not displayed as a donation
        # refactor this following line later when separating mocksite logic from mockevent object
        requests.get(url=MockEvent.mocksite_base_url + 'justgiving/increase/')
        config_adjustment.change_value(key='end_time', value=int(time.time()) + 30)
        time.sleep(4)
        bot = CharityBot(args=args)
        bot.initialise_bot()
        bot.start_bot()
        expected_string_two = 'Purrcat259 : ' + ChatBot.donation_string.format(Currency.GBP, 50.0, Currency.GBP, 150.52)
        chat_box_contents = get_twitch_chat_box_contents()
        assert expected_string_two in chat_box_contents


class TestFullAPIEvent:
    def test_full_event(self):
        ResetDB(db_path=repository_db_path, sql_path=repository_db_script_path)
        response = requests.get(MockEvent.mocksite_base_url + 'reset/')
        assert 200 == response.status_code
        config_adjustment.change_value(key='end_time', value=int(time.time()) + 10)
        args = parser.parse_args(['e2e_config', '--debug'])
        bot = CharityBot(args=args)
        bot.initialise_bot()
        # see that the overlay is functioning before starting
        overlay_url = api_full_url + 'overlay/{}'.format(event_config.get_value('internal_name'))
        response = requests.get(url=overlay_url)
        assert 200 == response.status_code
        bot.start_bot()
        # get the value from the overlay
        response = requests.get(url=overlay_url)
        assert 200 == response.status_code
        assert '<!DOCTYPE html>' in response.content.decode('utf-8')
        soup = BeautifulSoup(response.content, 'html.parser')
        amount_raised = soup.find('span', {'id': 'amount_raised'}).text.strip()
        assert '100' == amount_raised
