import os
import time

import requests

from charitybot2.events.event_config import EventConfiguration
from charitybot2.events.events import EventLoop, Event
from charitybot2.storage.events_db import EventsDB

current_directory = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_directory, 'data', 'events.db')
config_path = os.path.join(current_directory, 'data', 'config' + '.' + EventConfiguration.config_format)


class MockEvent(Event):
    mocksite_base_url = 'http://127.0.0.1:5000/'

    def __init__(self, mock_name, mock_end_time):
        super().__init__(config_path=config_path, db_path=db_path)
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


class TestEventRunThrough:
    def test_event_loop_changes_states_when_starting_and_finishing(self):
        test_event = MockEvent('test_one', time.time() + 20)
        test_event_loop = EventLoop(event=test_event, verbose=True)
        test_event_loop.start()
        assert test_event_loop.event.get_event_current_state() == EventsDB.event_completed_state

    def test_event_cycles_increment_properly(self):
        test_event = MockEvent('test_two', time.time() + 20)
        test_event_loop = EventLoop(event=test_event, verbose=True)
        test_event_loop.start()
        assert test_event_loop.loop_count == 4

    def test_event_amount_raised_changes_each_cycle(self):
        test_event = MockEvent('test_three', time.time() + 5)
        # first reset the amount on the mocksite so that the amount raised is back to default
        test_event.reset_mocksite()
        test_event_loop = EventLoop(event=test_event, verbose=True)
        test_event_loop.start()
        assert test_event_loop.event.get_amount_raised() == '200'
