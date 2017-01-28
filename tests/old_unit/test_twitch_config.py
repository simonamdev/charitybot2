import pytest
from charitybot2.botconfig.json_config import ConfigurationFileDoesNotExistException
from charitybot2.botconfig.twitch_config import TwitchAccountConfiguration
from tests.paths_for_tests import TestFilePath


def get_config_file_path(config_name):
    return TestFilePath().get_config_path('twitch', config_name + '.json')


class TestTwitchAccountConfigExistence:
    def test_twitch_account_config_does_exist(self):
        tac = TwitchAccountConfiguration(file_path=get_config_file_path('test_twitch_config'))
        assert True is tac.config_exists()

    @pytest.mark.parametrize('config_name', [
        '',
        'foobar'
    ])
    def test_twitch_account_config_does_not_exist_throws_exception(self, config_name):
        with pytest.raises(ConfigurationFileDoesNotExistException):
            TwitchAccountConfiguration(file_path=get_config_file_path(config_name))


tac = TwitchAccountConfiguration(file_path=get_config_file_path('test_twitch_config'))


class TestTwitchAccountConfigRetrieve:
    @pytest.mark.parametrize('expected,actual', [
        ('name',   tac.get_account_name()),
        ('id',     tac.get_client_id()),
        ('secret', tac.get_client_secret())
    ])
    def test_retrieval(self, expected, actual):
        assert expected == actual
