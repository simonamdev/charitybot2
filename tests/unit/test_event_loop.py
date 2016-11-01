import pytest

from charitybot2.charitybot2 import EventLoop
from charitybot2.events.event import Event, EventInvalidException, EventAlreadyFinishedException
from charitybot2.reporter.purrbot_config import purrbot_config
from charitybot2.reporter.twitch import TwitchAccount
from charitybot2.sources.justgiving import JustGivingScraper
from charitybot2.storage.db_handler import DBHandler
from tests.tests import ResetDB, TestFilePath

valid_config_path = TestFilePath().get_config_path('event', 'valid_config' + '.json')
btdonate_config_path = TestFilePath().get_config_path('event', 'btdonate_config' + '.json')
invalid_config_path = TestFilePath().get_config_path('event', 'invalid_config' + '.json')
already_finished_config_path = TestFilePath().get_config_path('event', 'already_finished_event_config' + '.json')

donations_db_path = TestFilePath().get_db_path('donations.db')
donations_db_init_script_path = TestFilePath().get_db_path('donations.sql')

db_handler = DBHandler(donations_db_path=donations_db_path)
valid_twitch_account = TwitchAccount(twitch_config=purrbot_config)


def setup_module():
    ResetDB(db_path=donations_db_path, sql_path=donations_db_init_script_path)


class ValidTestEvent(Event):
    def __init__(self):
        super().__init__(config_path=valid_config_path, db_handler=db_handler)


class TestEventLoopValidity:
    def test_initialise_with_bad_event_throws_exception(self):
        with pytest.raises(EventInvalidException):
            el = EventLoop(event=None, twitch_account=valid_twitch_account)

    def test_initialise_with_valid_event(self):
        el = EventLoop(event=ValidTestEvent(), twitch_account=valid_twitch_account)

    def test_initialise_not_implemented_btdonate_scraper_throws_exception(self):
        with pytest.raises(NotImplementedError):
            e = Event(config_path=btdonate_config_path, db_handler=db_handler)
            el = EventLoop(event=e, twitch_account=None)

    def test_valid_event_loop_scraper_is_of_type_justgivingscraper(self):
        el = EventLoop(event=ValidTestEvent(), twitch_account=valid_twitch_account)
        assert isinstance(el.scraper, JustGivingScraper)

    def test_starting_already_complete_event_throws_exception(self):
        with pytest.raises(EventAlreadyFinishedException):
            e = Event(config_path=already_finished_config_path, db_handler=db_handler)
            el = EventLoop(event=e, twitch_account=valid_twitch_account)


class TestEventLoopAmountRetrieve:
    # Test is definitely flaky
    def test_event_loop_retrieves_amount_successfully(self):
        el = EventLoop(event=ValidTestEvent(), twitch_account=valid_twitch_account, debug=True)
        el.check_for_donation()
        assert el.event.get_amount_raised() == 35487.0
