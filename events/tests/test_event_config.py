import pytest
import os
from events import event_config
from time import sleep

current_directory = os.path.dirname(os.path.abspath(__file__))
valid_config_path = os.path.join(current_directory, 'valid_test_config.json')
invalid_json_config_path = os.path.join(current_directory, 'invalid_json_test_config.json')
invalid_config_path = os.path.join(current_directory, 'invalid_test_config.json')
empty_config_path = os.path.join(current_directory, 'empty_test_config.json')
no_source_config_path = os.path.join(current_directory, 'empty_source_event_config.json')


def test_event_config_does_not_exist():
    with pytest.raises(event_config.EventConfigFileDoesNotExistException):
        ec = event_config.EventConfiguration(file_path='pfdkgopdfkg')


def test_event_config_does_exist():
    ec = event_config.EventConfiguration(file_path=valid_config_path)
    assert ec.config_exists() is True


def test_empty_event_config():
    ec = event_config.EventConfiguration(file_path=empty_config_path)
    with pytest.raises(event_config.InvalidEventConfigException):
        ec.read_config()


def test_invalid_format_event_config():
    ec = event_config.EventConfiguration(file_path=invalid_json_config_path)
    with pytest.raises(event_config.InvalidEventConfigException):
        ec.read_config()


def test_event_config_read_time_changing():
    ec = event_config.EventConfiguration(file_path=valid_config_path)
    ec.read_config()
    first_read_time = ec.get_config_last_read_time()
    assert not first_read_time == 0
    sleep(0.25)
    ec.read_config()
    second_read_time = ec.get_config_last_read_time()
    assert not first_read_time == second_read_time


def test_valid_formatted_but_invalid_content_event_config():
    ec = event_config.EventConfiguration(file_path=invalid_config_path)
    with pytest.raises(event_config.InvalidEventConfigException):
        ec.read_config()


def test_retrieving_non_existent_config_field_throws_exception():
    ec = event_config.EventConfiguration(file_path=valid_config_path)
    with pytest.raises(event_config.EventConfigFieldDoesNotExistException):
        ec.get_config_value(value_name='test')


def test_retrieving_integer_when_requesting_number_key_values():
    ec = event_config.EventConfiguration(file_path=valid_config_path)
    values = []
    for key in ec.number_keys:
        values.append(ec.get_config_value(value_name=key))
    for value in values:
        assert isinstance(value, int)


def test_retrieving_non_integer_when_requesting_non_number_key_values():
    ec = event_config.EventConfiguration(file_path=valid_config_path)
    values = []
    all_keys = ec.keys_required
    non_number_keys = [key for key in all_keys if key not in ec.number_keys]
    for key in non_number_keys:
        values.append(ec.get_config_value(value_name=key))
    for value in values:
        assert not isinstance(value, int)


def test_no_defined_sources_throwing_invalid_config_exception():
    ec = event_config.EventConfiguration(file_path=no_source_config_path)
    with pytest.raises(event_config.InvalidEventConfigException):
        ec.read_config()


def test_retrieving_list_when_requesting_lift_key_values():
    ec = event_config.EventConfiguration(file_path=valid_config_path)
    values = []
    for key in ec.list_keys:
        values.append(ec.get_config_value(value_name=key))
    for value in values:
        assert isinstance(value, list)

