import os

import charitybot2.events.event_config as event_config
import charitybot2.sources.sources as sources

current_directory = os.path.dirname(os.path.abspath(__file__))
config_directory = os.path.join(current_directory, 'configs')
good_source_path = os.path.join(config_directory, 'good_source_event_config.json')
bad_source_path = os.path.join(config_directory, 'bad_source_event_config.json')

sources_available = sources.sources_available


class TestEventSourcesValidity:
    def test_bad_sources_in_event_config_throws_exception(self):
        ec = event_config.EventConfiguration(file_path=bad_source_path)
        bad_sources = ec.get_config_value(value_name='sources_required')
        for source in sources_available:
            assert source not in bad_sources

    def test_valid_sources_in_event_config_file(self):
        ec = event_config.EventConfiguration(file_path=good_source_path)
        config_sources = ec.get_config_value(value_name='sources_required')
        for source in config_sources:
            assert source in sources_available
