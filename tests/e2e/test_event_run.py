import time
import requests

from charitybot2.charitybot2 import EventLoop
from charitybot2.events.event import Event
from charitybot2.events.event_config import EventConfiguration
from charitybot2.paths import mocksite_path
from charitybot2.reporter.purrbot_config import purrbot_config
from charitybot2.reporter.twitch import TwitchAccount
from charitybot2.sources.mocks.mocksite import mocksite_full_url
from charitybot2.storage.db_handler import DBHandler
from tests.tests import ResetDB, ServiceTest, TestFilePath

config_path = TestFilePath().get_config_path('config' + '.' + EventConfiguration.config_format)
events_db_path = TestFilePath().get_db_path('events.db')
events_db_init_script_path = TestFilePath().get_db_path('events.sql')
donations_db_path = TestFilePath().get_db_path('donations.db')
donations_db_init_script_path = TestFilePath().get_db_path('donations.sql')


ResetDB(db_path=donations_db_path, sql_path=donations_db_init_script_path)

purrbot = TwitchAccount(twitch_config=purrbot_config)


class MockEvent(Event):
    mocksite_base_url = mocksite_full_url

    def __init__(self, mock_name, mock_end_time):
        super().__init__(config_path=config_path, db_handler=DBHandler(donations_db_path=donations_db_path, debug=True))
        self.mock_name = mock_name
        self.mock_end_time = mock_end_time

    def get_event_name(self):
        return self.mock_name

    def get_end_time(self):
        return self.mock_end_time

    def get_source_url(self):
        return self.mocksite_base_url + 'justgiving/'

    def reset_mocksite(self):
        requests.get(url=self.mocksite_base_url + 'reset/')


class NonReportingLoop(EventLoop):
    def __init__(self, event, twitch_account, debug=False):
        super().__init__(event, twitch_account, debug)

    def report_new_donation(self, donation):
        pass


service_test = ServiceTest('Donations Mocksite', MockEvent.mocksite_base_url, service_path=mocksite_path)


def setup_module():
    service_test.start_service()
    r = requests.get(url=mocksite_full_url + 'reset')
    assert 200 == r.status_code


def teardown_module():
    service_test.stop_service()


class TestEventRunThrough:
    def test_event_cycles_increment_properly(self):
        test_event = MockEvent('test_two', time.time() + 5)
        test_event_loop = NonReportingLoop(event=test_event, twitch_account=purrbot, debug=True)
        test_event_loop.start()
        assert 1 == test_event_loop.loop_count

    def test_event_amount_raised_changes_each_cycle(self):
        test_event = MockEvent('test_three', time.time() + 5)
        # first reset the amount on the mocksite so that the amount raised is back to default
        test_event.reset_mocksite()
        test_event_loop = NonReportingLoop(event=test_event, twitch_account=purrbot, debug=True)
        test_event_loop.start()
        assert 200.52 == test_event_loop.event.get_amount_raised()

    # def test_donation_message_appears_every_cycle(self):
    #     test_event = MockEvent('test_three', time.time() + 10)
    #     test_event.reset_mocksite()
    #     test_event_loop = NonReportingLoop(event=test_event, twitch_account=purrbot, debug=True)
