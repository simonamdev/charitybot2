import pytest
import os
from events import event_config

valid_config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'valid_test_config.json')
invalid_config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'invalid_test_config.json')
empty_config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'empty_test_config.json')


def test_event_config_does_not_exist():
    with pytest.raises(event_config.EventConfigFileDoesNotExist):
        ec = event_config.EventConfiguration(file_path='pfdkgopdfkg')


def test_event_config_does_exist():
    ec = event_config.EventConfiguration(file_path=valid_config_path)
    assert ec.config_exists() is True


def test_empty_event_config():
    ec = event_config.EventConfiguration(file_path=empty_config_path)
    with pytest.raises(event_config.InvalidEventConfiguration):
        ec.read_config()


def test_invalid_event_config():
    ec = event_config.EventConfiguration(file_path=invalid_config_path)
    with pytest.raises(event_config.InvalidEventConfiguration):
        ec.read_config()
