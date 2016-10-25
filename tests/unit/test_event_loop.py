import os

import pytest

import charitybot2.events.event_config as event_config
from charitybot2.events.event import Event, EventInvalidException, EventAlreadyFinishedException
from charitybot2.charitybot2 import EventLoop
from charitybot2.sources.justgiving import JustGivingScraper

current_directory = os.path.dirname(os.path.abspath(__file__))
events_db_path = os.path.join(current_directory, 'db', 'test_events.db')
valid_config_path = os.path.join(current_directory, 'configs', 'valid_config' + '.' + event_config.EventConfiguration.config_format)
btdonate_config_path = os.path.join(current_directory, 'configs', 'btdonate_config' + '.' + event_config.EventConfiguration.config_format)
invalid_config_path = os.path.join(current_directory, 'configs', 'invalid_config' + '.' + event_config.EventConfiguration.config_format)
already_finished_config_path = os.path.join(current_directory, 'configs', 'already_finished_event_config' + '.' + event_config.EventConfiguration.config_format)


class ValidTestEvent(Event):
    def __init__(self):
        super().__init__(config_path=valid_config_path, db_path=events_db_path)


class TestEventLoopValidity:
    def test_initialise_with_bad_event_throws_exception(self):
        with pytest.raises(EventInvalidException):
            el = EventLoop(event=None)

    def test_initialise_with_valid_event(self):
        el = EventLoop(event=ValidTestEvent())

    def test_initialise_not_implemented_btdonate_scraper_throws_exception(self):
        with pytest.raises(NotImplementedError):
            e = Event(config_path=btdonate_config_path, db_path=events_db_path)
            el = EventLoop(event=e)

    def test_valid_event_loop_scraper_is_of_type_justgivingscraper(self):
        el = EventLoop(event=ValidTestEvent())
        assert isinstance(el.scraper, JustGivingScraper)

    def test_starting_already_complete_event_throws_exception(self):
        with pytest.raises(EventAlreadyFinishedException):
            e = Event(config_path=already_finished_config_path, db_path=events_db_path)
            el = EventLoop(event=e)


class TestEventLoopAmountRetrieve:
    # Test is definitely flaky
    def test_event_loop_retrieves_amount_successfully(self):
        el = EventLoop(event=ValidTestEvent())
        el.check_for_donation()
        assert el.event.get_amount_raised() == '£35,487'
