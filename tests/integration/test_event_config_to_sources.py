import os

from charitybot2.events.event_config import EventConfiguration
from charitybot2.sources.sources import source_names_supported

current_directory = os.path.dirname(os.path.abspath(__file__))
config_directory = os.path.join(current_directory, 'configs')
good_source_path = os.path.join(config_directory, 'good_source_event_config.json')
bad_source_path = os.path.join(config_directory, 'bad_source_event_config.json')


class TestEventSourcesValidity:
    def test_bad_source_names_in_event_config_throws_exception(self):
        ec = EventConfiguration(file_path=bad_source_path)
        bad_sources = ec.get_config_value(value_name='sources_required')
        for source in bad_sources:
            assert source['name'] not in source_names_supported

    def test_valid_source_names_in_event_config_file(self):
        ec = EventConfiguration(file_path=good_source_path)
        config_sources = ec.get_config_value(value_name='sources_required')
        for source in config_sources:
            assert source['name'] in source_names_supported

    def test_source_url_names_in_event_config_are_not_empty(self):
        ec = EventConfiguration(file_path=good_source_path)
        config_sources = ec.get_config_value(value_name='sources_required')
        for source in config_sources:
            assert not source['url_name'] == ''
