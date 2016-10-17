import os

from charitybot2.events.event_config import EventConfiguration
from charitybot2.events.events import EventLoop, Event

current_directory = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_directory, 'data', 'events.db')
config_path = os.path.join(current_directory, 'data', 'config' + '.' + EventConfiguration.config_format)


def test_event_cycle_count():
    test_event = Event(config_path=config_path, db_path=db_path)
    test_event_loop = EventLoop(event=test_event)
