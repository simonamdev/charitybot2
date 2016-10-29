import pytest
from charitybot2.json_config import ConfigurationFileDoesNotExistException, JSONConfigurationFile
from tests.tests import TestFilePath


def get_config_file_path(config_name):
    return TestFilePath().get_config_path('', config_name + '.json')


class TestConfigFileExistence:
    def test_config_files_does_not_exist_throws_exception(self):
        with pytest.raises(ConfigurationFileDoesNotExistException):
            conf = JSONConfigurationFile(file_path='fgdfgeg')
