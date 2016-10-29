import pytest
from charitybot2.json_config import ConfigurationFileDoesNotExistException, JSONConfigurationFile, InvalidConfigurationException
from tests.tests import TestFilePath


def get_config_file_path(config_name):
    return TestFilePath().get_config_path('base', config_name + '.json')


class TestConfigFileExistence:
    def test_config_file_does_not_exist_throws_exception(self):
        with pytest.raises(ConfigurationFileDoesNotExistException):
            conf = JSONConfigurationFile(file_path='fgdfgeg')

    def test_config_file_exists(self):
        conf = JSONConfigurationFile(file_path=get_config_file_path('valid_config'))
        assert True is conf.config_exists()


class TestConfigValidity:
    def test_empty_config_file_throws_exception(self):
        with pytest.raises(InvalidConfigurationException):
            conf = JSONConfigurationFile(file_path=get_config_file_path('empty_config'))

