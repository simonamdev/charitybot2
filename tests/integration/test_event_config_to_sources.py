import os

from charitybot2.events.event_config import EventConfiguration
from charitybot2.sources.sources import source_names_supported

current_directory = os.path.dirname(os.path.abspath(__file__))
config_directory = os.path.join(current_directory, 'configs')
good_source_path = os.path.join(config_directory, 'good_source_event_config.json')
bad_source_path = os.path.join(config_directory, 'bad_source_event_config.json')


class TestEventSourcesValidity:
    def test_invalid_source_url_in_event_config_throws_exception(self):
        ec = EventConfiguration(file_path=bad_source_path)
        bad_source_url = ec.get_config_value(value_name='source_url')
        for supported_source_name in source_names_supported:
            assert supported_source_name not in bad_source_url

    def test_valid_source_url_in_event_config_file(self):
        ec = EventConfiguration(file_path=good_source_path)
        source_url = ec.get_config_value(value_name='source_url')
        assert 'justgiving' in source_url
