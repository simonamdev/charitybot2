import pytest
from charitybot2.reporter.twitch_config import IllegalConfigValueException, TwitchConfig


class TestTwitchConfigValidity:
    def test_passing_empty_client_id_throws_exception(self):
        with pytest.raises(IllegalConfigValueException):
            TwitchConfig('name', client_id='', client_secret='secret')

    def test_passing_empty_client_secret_throws_exception(self):
        with pytest.raises(IllegalConfigValueException):
            TwitchConfig('name', client_id='id', client_secret='')

    def test_passing_empty_account_name_throws_exception(self):
        with pytest.raises(IllegalConfigValueException):
            TwitchConfig('', 'id', 'secret')


class TestTwitchReturningValues:
    def test_getting_values(self):
        tc = TwitchConfig('name', client_id='id', client_secret='secret')
        assert 'name' == tc.get_account_name()
        assert 'id' == tc.get_client_id()
        assert 'secret' == tc.get_client_secret()
