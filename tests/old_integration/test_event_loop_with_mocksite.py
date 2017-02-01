import time

import pytest
from charitybot2.botconfig.event_config import EventConfigurationFromFile, EventConfigurationCreator
from charitybot2.events.event_loop import EventLoop
from charitybot2.events.event import Event
from charitybot2.sources.mocks.mocksite import mocksite_full_url, mock_justgiving_fundraising_url
from tests.paths_for_tests import valid_config_path, repository_db_path, repository_db_script_path
from tests.mocks import ResetDB, MockFundraisingWebsite


class MockEvent(Event):
    mocksite_base_url = mocksite_full_url

    def __init__(self, config_path, mock_name, mock_end_time):
        config_values = EventConfigurationFromFile(file_path=config_path).get_config_data()
        config_values['source_url'] = mock_justgiving_fundraising_url
        config_values['internal_name'] = mock_name
        config_values['end_time'] = mock_end_time
        config_values['update_delay'] = 2
        mock_event_config = EventConfigurationCreator(config_values=config_values).get_event_configuration()
        super().__init__(event_configuration=mock_event_config, db_path=repository_db_path)
        self.mock_name = mock_name
        self.mock_end_time = mock_end_time

    def get_internal_name(self):
        return self.mock_name

    def get_end_time(self):
        return self.mock_end_time


mock_fundraising_website = MockFundraisingWebsite(fundraiser_name='justgiving')


def setup_module():
    ResetDB(db_path=repository_db_path, sql_path=repository_db_script_path)
    mock_fundraising_website.start()
    mock_fundraising_website.reset_amount()


def teardown_module():
    mock_fundraising_website.stop()


class TestEventRunThrough:
    def test_getting_new_amount_properly_formatted(self):
        test_event = MockEvent(config_path=valid_config_path, mock_name='test_one', mock_end_time=int(time.time()) + 10)
        el = EventLoop(event=test_event, debug=True)
        # 2 loops
        mock_fundraising_website.increase_amount()
        mock_fundraising_website.increase_amount()
        assert 200.52 == el.get_new_amount()

    @pytest.mark.parametrize('cycle_count', [
        1,
        2,
        3
    ])
    def test_event_cycles_increment_properly(self, cycle_count):
        test_event = MockEvent(
            config_path=valid_config_path,
            mock_name='test_two',
            mock_end_time=int(time.time()) + (2 * cycle_count))
        test_event_loop = EventLoop(event=test_event, debug=True)
        test_event_loop.start()
        assert cycle_count == test_event_loop.loop_count

    @pytest.mark.parametrize('cycle_count', [
        1,
        2,
        3
    ])
    def test_event_amount_raised_changes_each_cycle(self, cycle_count):
        increment_amount = 50
        test_event = MockEvent(
            config_path=valid_config_path,
            mock_name='test_three',
            mock_end_time=int(time.time()) + (2 * cycle_count))
        # first reset the amount on the mocksite so that the amount raised is back to default
        mock_fundraising_website.reset_amount()
        for i in range(0, cycle_count):
            mock_fundraising_website.increase_amount()
        test_event_loop = EventLoop(event=test_event, debug=True)
        test_event_loop.start()
        expected_amount_raised = round(100.52 + (increment_amount * cycle_count), 2)
        assert expected_amount_raised == test_event_loop.event.get_amount_raised()

    def test_event_amount_raising_only_when_amount_is_different(self):
        test_event = MockEvent(config_path=valid_config_path, mock_name='event_loop_test', mock_end_time=int(time.time()) + 10)
        mock_fundraising_website.reset_amount()
        test_event_loop = EventLoop(event=test_event, debug=True)
        # avoid first check
        test_event_loop.check_for_donation()
        # do two cycles without changing amount, amount should be the same
        test_event_loop.check_for_donation()
        assert 100.52 == test_event_loop.event.get_amount_raised()
        test_event_loop.check_for_donation()
        assert 100.52 == test_event_loop.event.get_amount_raised()
        # Change the amount
        mock_fundraising_website.increase_amount()
        test_event_loop.check_for_donation()
        assert 150.52 == test_event_loop.event.get_amount_raised()
