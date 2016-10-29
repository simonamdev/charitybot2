import pytest
from charitybot2.reporter.twitch_config import TwitchAccountConfiguration, TwitchAccountConfigurationFileDoesNotExistException
from tests.tests import TestFilePath


def get_config_file_path(config_name):
    return TestFilePath().get_config_path('twitch', config_name + '.' + TwitchAccountConfiguration.config_format)


class TestTwitchAccountConfigExistence:
    def test_twitch_account_config_does_not_exist_throws_exception(self):
        with pytest.raises(TwitchAccountConfigurationFileDoesNotExistException):
            tac = TwitchAccountConfiguration(file_path='dsoijoisjfd')

    def test_twitch_account_config_does_exist(self):
        tac = TwitchAccountConfiguration(file_path=get_config_file_path('valid_twitch_config'))
        assert True is tac.config_exists()

#
#
# class TestTwitchConfigValidity:
#     def test_passing_empty_client_id_throws_exception(self):
#         with pytest.raises(IllegalConfigValueException):
#             TwitchAccountConfiguration('name', client_id='', client_secret='secret')
#
#     def test_passing_empty_client_secret_throws_exception(self):
#         with pytest.raises(IllegalConfigValueException):
#             TwitchAccountConfiguration('name', client_id='id', client_secret='')
#
#     def test_passing_empty_account_name_throws_exception(self):
#         with pytest.raises(IllegalConfigValueException):
#             TwitchAccountConfiguration('', 'id', 'secret')
#
#
# class TestTwitchReturningValues:
#     def test_getting_values(self):
#         tc = TwitchAccountConfiguration('name', client_id='id', client_secret='secret')
#         assert 'name' == tc.get_account_name()
#         assert 'id' == tc.get_client_id()
#         assert 'secret' == tc.get_client_secret()
