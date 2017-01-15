import copy
import pytest

from charitybot2.botconfig.event_config import EventConfigurationFromFile, EventConfigurationCreator
from charitybot2.events.event_loop import EventLoop
from charitybot2.events.event import Event, EventInvalidException
from charitybot2.reporter.purrbot_config import purrbot_config
from charitybot2.reporter.twitch import TwitchAccount
from charitybot2.sources.justgiving import JustGivingScraper
from tests.restters_for_tests import ResetDB, TestFilePath

valid_config_path = TestFilePath().get_config_path('event', 'valid_config' + '.json')
valid_event_config_values = EventConfigurationFromFile(file_path=valid_config_path).get_config_data()
valid_event_configuration = EventConfigurationCreator(config_values=valid_event_config_values).get_event_configuration()

btdonate_config_values = copy.deepcopy(valid_event_config_values)
btdonate_config_values['source_url'] = 'https://mydonate.bt.com/fundraisers/acpi'
btdonate_configuration = EventConfigurationCreator(config_values=btdonate_config_values).get_event_configuration()

db_path = TestFilePath().get_repository_db_path()
db_script_path = TestFilePath().get_repository_script_path()

valid_twitch_account = TwitchAccount(twitch_config=purrbot_config)


def setup_module():
    ResetDB(db_path=db_path, sql_path=db_script_path)


class ValidTestEvent(Event):
    def __init__(self):
        super().__init__(event_configuration=valid_event_configuration, db_path=db_path)


class TestEventLoopValidity:
    def test_initialise_with_bad_event_throws_exception(self):
        with pytest.raises(EventInvalidException):
            el = EventLoop(event=None, debug=True)

    def test_initialise_with_valid_event(self):
            el = EventLoop(event=ValidTestEvent(), debug=True)

    def test_initialise_not_implemented_btdonate_scraper_throws_exception(self):
        with pytest.raises(NotImplementedError):
            e = Event(event_configuration=btdonate_configuration, db_path=db_path)
            el = EventLoop(event=e, debug=True)

    def test_valid_event_loop_scraper_is_of_type_justgivingscraper(self):
        el = EventLoop(event=ValidTestEvent(), debug=True)
        assert isinstance(el.scraper, JustGivingScraper)

    def test_event_loop_donations_not_stored_yet(self):
        el = EventLoop(event=ValidTestEvent(), debug=True)
        assert False is el.donations_already_present()
