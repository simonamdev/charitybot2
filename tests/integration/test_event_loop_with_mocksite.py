import time

import requests
from charitybot2.botconfig.event_config import EventConfigurationFromFile, EventConfigurationCreator
from charitybot2.events.event_loop import EventLoop
from charitybot2.events.event import Event
from charitybot2.paths import mocksite_path
from charitybot2.sources.mocks.mocksite import mocksite_full_url
from tests.paths_for_tests import valid_config_path, repository_db_path, repository_db_script_path
from tests.mocks import ResetDB, ServiceTest


class MockEvent(Event):
    mocksite_base_url = mocksite_full_url

    def __init__(self, config_path, mock_name, mock_end_time):
        config_values = EventConfigurationFromFile(file_path=config_path).get_config_data()
        config_values['internal_name'] = mock_name
        config_values['end_time'] = mock_end_time
        mock_event_config = EventConfigurationCreator(config_values=config_values).get_event_configuration()
        super().__init__(event_configuration=mock_event_config, db_path=repository_db_path)
        self.mock_name = mock_name
        self.mock_end_time = mock_end_time

    def get_internal_name(self):
        return self.mock_name

    def get_end_time(self):
        return self.mock_end_time

    def get_source_url(self):
        return self.mocksite_base_url + 'justgiving/'

    def increase_mocksite_amount(self):
        requests.get(url=self.get_source_url() + 'increase/')

    def reset_mocksite(self):
        requests.get(url=self.mocksite_base_url + 'reset/')

service_test = ServiceTest(
    service_name='Donations Mocksite',
    service_url=MockEvent.mocksite_base_url,
    service_path=mocksite_path,
    enter_debug=False)


def setup_module():
    ResetDB(db_path=repository_db_path, sql_path=repository_db_script_path)
    service_test.start_service()
    r = requests.get(url=mocksite_full_url + 'reset')
    assert 200 == r.status_code


def teardown_module():
    service_test.stop_service()


class TestEventRunThrough:
    def test_getting_new_amount_properly_formatted(self):
        test_event = MockEvent(config_path=valid_config_path, mock_name='test_one', mock_end_time=int(time.time()) + 10)
        el = EventLoop(event=test_event, debug=True)
        # 2 loops
        test_event.increase_mocksite_amount()
        test_event.increase_mocksite_amount()
        assert 200.52 == el.get_new_amount()

    def test_event_cycles_increment_properly(self):
        test_event = MockEvent(config_path=valid_config_path, mock_name='test_two', mock_end_time=int(time.time()) + 5)
        test_event_loop = EventLoop(event=test_event, debug=True)
        test_event_loop.start()
        assert 1 == test_event_loop.loop_count

    def test_event_amount_raised_changes_each_cycle(self):
        test_event = MockEvent(config_path=valid_config_path, mock_name='test_three', mock_end_time=int(time.time()) + 10)
        # first reset the amount on the mocksite so that the amount raised is back to default
        test_event.reset_mocksite()
        # 3 cycles
        test_event.increase_mocksite_amount()
        test_event.increase_mocksite_amount()
        test_event.increase_mocksite_amount()
        test_event_loop = EventLoop(event=test_event, debug=True)
        test_event_loop.start()
        assert 250.52 == test_event_loop.event.get_amount_raised()

    def test_event_amount_raising_only_when_amount_is_different(self):
        test_event = MockEvent(config_path=valid_config_path, mock_name='event_loop_test', mock_end_time=int(time.time()) + 10)
        test_event.reset_mocksite()
        test_event_loop = EventLoop(event=test_event, debug=True)
        # avoid first check
        test_event_loop.check_for_donation()
        # do two cycles without changing amount, amount should be the same
        test_event_loop.check_for_donation()
        assert 100.52 == test_event_loop.event.get_amount_raised()
        test_event_loop.check_for_donation()
        assert 100.52 == test_event_loop.event.get_amount_raised()
        # Change the amount
        # response = requests.get(test_event.get_source_url())
        # assert 200 == response.status_code
        test_event.increase_mocksite_amount()
        test_event_loop.check_for_donation()
        assert 150.52 == test_event_loop.event.get_amount_raised()
