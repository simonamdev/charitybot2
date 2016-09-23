import pytest
import os
from events import eventConfig


def test_event_config_does_not_exist():
    ec = eventConfig.EventConfiguration(file_path='pfdkgopdfkg')
    assert ec.config_exists() is False


def test_event_config_does_exist():
    current_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_path, 'test_config.json')
    ec = eventConfig.EventConfiguration(file_path=file_path)
    assert ec.config_exists() is True
