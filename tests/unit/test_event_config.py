from charitybot2.config.event_config import EventConfiguration
from tests.tests import TestFilePath


def get_config_file_path(config_name):
    return TestFilePath().get_config_path('event', config_name + '.json')

class TestEventConfigExistence:
    def test_event_config_does_exist(self):
        ec = EventConfiguration(file_path=get_config_file_path('valid_config'))
        assert ec.config_exists() is True


class TestEventConfigRetrieve:
    def test_source_url_is_valid_url(self):
        import re
        url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        ec = EventConfiguration(file_path=get_config_file_path('valid_config'))
        source_url = ec.get_value('source_url')
        urls = re.findall(url_regex, source_url)
        assert len(urls) == 1

    def test(self):
        ec = EventConfiguration(file_path=get_config_file_path('valid_config'))
        for key in EventConfiguration.number_keys:
            assert isinstance(ec.get_value(key), int)
