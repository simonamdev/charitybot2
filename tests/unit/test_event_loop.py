import copy
import pytest

from charitybot2.botconfig.event_config import EventConfigurationFromFile, EventConfigurationCreator
from charitybot2.events.event_loop import EventLoop
from charitybot2.events.event import Event, EventInvalidException
from charitybot2.sources.justgiving import JustGivingScraper
from charitybot2.sources.mocks.mocksite import mock_justgiving_fundraising_url, mock_mydonate_teams_url
from charitybot2.sources.mydonate import MyDonateScraper
from tests.paths_for_tests import valid_config_path, repository_db_path, repository_db_script_path
from tests.mocks import ResetDB

valid_event_config_values = EventConfigurationFromFile(file_path=valid_config_path).get_config_data()


def get_updated_configuration(updates=None):
    no_donations_config_values = copy.deepcopy(valid_event_config_values)
    if updates is not None:
        no_donations_config_values.update(updates)
    return EventConfigurationCreator(no_donations_config_values).get_event_configuration()


def setup_module():
    ResetDB(db_path=repository_db_path, sql_path=repository_db_script_path)


class ValidTestEvent(Event):
    def __init__(self, event_configuration=get_updated_configuration()):
        super().__init__(event_configuration=event_configuration, db_path=repository_db_path)


class TestEventLoopValidity:
    def test_initialise_with_bad_event_throws_exception(self):
        with pytest.raises(EventInvalidException):
            el = EventLoop(event=None, debug=True)

    def test_initialise_with_valid_event(self):
            el = EventLoop(event=ValidTestEvent(), debug=True)

    @pytest.mark.parametrize('event_configuration,expected_type', [
        (get_updated_configuration({'source_url': mock_justgiving_fundraising_url}), JustGivingScraper),
        (get_updated_configuration({'source_url': mock_mydonate_teams_url}), MyDonateScraper)
    ])
    def test_scraper_types_according_to_url(self, event_configuration, expected_type):
        el = EventLoop(event=ValidTestEvent(event_configuration=event_configuration), debug=True)
        assert isinstance(el.scraper, expected_type)

    def test_current_amount_is_equal_to_starting_amount_when_no_donations_present(self):
        no_donations_config = get_updated_configuration({'internal_name': 'NoDonations'})
        no_donations_event = Event(event_configuration=no_donations_config, db_path=repository_db_path)
        el = EventLoop(event=no_donations_event, debug=True)
        assert 100 == el.event.get_amount_raised()
