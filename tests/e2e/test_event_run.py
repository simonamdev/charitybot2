import os
import time

from charitybot2.events.event_config import EventConfiguration
from charitybot2.events.events import EventLoop, Event
from charitybot2.storage.events_db import EventsDB

current_directory = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_directory, 'data', 'events.db')
config_path = os.path.join(current_directory, 'data', 'config' + '.' + EventConfiguration.config_format)


class MockEvent(Event):
    def __init__(self, mock_end_time):
        super().__init__(config_path=config_path, db_path=db_path)
        self.mock_end_time = mock_end_time

    def get_end_time(self):
        return self.mock_end_time


class TestEvenRunThrough:
    def test_event_loop_changes_states_when_starting_and_finishing(self):
        test_event = MockEvent(time.time() + 20)
        test_event_loop = EventLoop(event=test_event, verbose=True)
        test_event_loop.start()
        assert test_event_loop.event.get_event_current_state() == EventsDB.event_completed_state

