from charitybot2.botconfig.twitch_config import TwitchAccountConfiguration
from tests.tests import TestFilePath


def get_config_file_path(config_name):
    return TestFilePath().get_config_path('twitch', config_name + '.json')


class TestTwitchAccountConfigExistence:
    def test_twitch_account_config_does_exist(self):
        tac = TwitchAccountConfiguration(file_path=get_config_file_path('test_twitch_config'))
        assert True is tac.config_exists()


class TestTwitchAccountConfigRetrieve:
    tac = TwitchAccountConfiguration(file_path=get_config_file_path('test_twitch_config'))

    def test_get_name(self):
        assert 'name' == self.tac.get_account_name()

    def test_get_id(self):
        assert 'id' == self.tac.get_client_id()

    def test_get_secret(self):
        assert 'secret' == self.tac.get_client_secret()
