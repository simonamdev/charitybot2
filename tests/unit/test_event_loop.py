import os

import pytest

import charitybot2.events.event_config as event_config
from charitybot2.events.events import Event, EventLoop, EventInvalidException
from charitybot2.sources.justgiving import JustGivingScraper

current_directory = os.path.dirname(os.path.abspath(__file__))
events_db_path = os.path.join(current_directory, 'db', 'test_events.db')
valid_config_path = os.path.join(current_directory, 'configs', 'valid_config' + '.' + event_config.EventConfiguration.config_format)
btdonate_config_path = os.path.join(current_directory, 'configs', 'btdonate_config' + '.' + event_config.EventConfiguration.config_format)
invalid_config_path = os.path.join(current_directory, 'configs', 'invalid_config' + '.' + event_config.EventConfiguration.config_format)


class ValidTestEvent(Event):
    def __init__(self):
        super().__init__(config_path=valid_config_path)


class TestEventLoopValidity:
    def test_initialise_with_bad_event_throws_exception(self):
        with pytest.raises(EventInvalidException):
            el = EventLoop(event=None, db_path=events_db_path)

    def test_initialise_with_valid_event_throws_exception(self):
        el = EventLoop(event=ValidTestEvent(), db_path=events_db_path)
        el.initialise_db_interface()
        el.initialise_scraper()

    def test_initialise_not_implemented_btdonate_scraper_throws_exception(self):
        with pytest.raises(NotImplementedError):
            e = Event(config_path=btdonate_config_path)
            el = EventLoop(event=e, db_path=events_db_path)
            el.initialise_scraper()

    def test_valid_eventloop_scraper_is_of_type_justgivingscraper(self):
        el = EventLoop(event=ValidTestEvent(), db_path=events_db_path)
        el.initialise_db_interface()
        el.initialise_scraper()
        assert isinstance(el.scraper, JustGivingScraper)


