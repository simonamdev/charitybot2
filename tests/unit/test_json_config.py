import pytest
from charitybot2.botconfig.json_config import ConfigurationFileDoesNotExistException, JSONConfigurationFile, InvalidConfigurationException, \
    ConfigurationFieldDoesNotExistException
from tests.restters_for_tests import TestFilePath

valid_config_keys = ("key1", "key2", "key3")
invalid_config_keys = ("test1", "test2")


def get_config_file_path(config_name):
    return TestFilePath().get_config_path('base', config_name + '.json')


class TestConfigFileExistence:
    def test_config_file_does_not_exist_throws_exception(self):
        with pytest.raises(ConfigurationFileDoesNotExistException):
            conf = JSONConfigurationFile(file_path='fgdfgeg', keys_required=())

    def test_config_file_exists(self):
        conf = JSONConfigurationFile(file_path=get_config_file_path('valid_config'), keys_required=valid_config_keys)
        assert True is conf.config_exists()


class TestConfigValidity:
    def test_empty_config_file_throws_exception(self):
        with pytest.raises(InvalidConfigurationException):
            conf = JSONConfigurationFile(file_path=get_config_file_path('empty_config'), keys_required=())

    def test_invalid_formatted_config_file_throws_exception(self):
        with pytest.raises(InvalidConfigurationException):
            conf = JSONConfigurationFile(file_path=get_config_file_path('invalid_formatted_config'), keys_required=())

    def test_valid_formatted_but_invalid_content_config_throws_exception(self):
        with pytest.raises(InvalidConfigurationException):
            conf = JSONConfigurationFile(file_path=get_config_file_path('invalid_config'), keys_required=invalid_config_keys)


class TestConfigRetrieve:
    def test_retrieving_non_existent_field_throws_exception(self):
        conf = JSONConfigurationFile(file_path=get_config_file_path('valid_config'), keys_required=valid_config_keys)
        with pytest.raises(ConfigurationFieldDoesNotExistException):
            conf.get_value('test')

    def test_retrieving_existent_field_returns_expected_value(self):
        conf = JSONConfigurationFile(file_path=get_config_file_path('valid_config'), keys_required=valid_config_keys)
        assert 'value1' == conf.get_value('key1')
