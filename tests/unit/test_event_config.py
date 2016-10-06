import os
import pytest
import charitybot2.events.event_config as event_config
from time import sleep


current_directory = os.path.dirname(os.path.abspath(__file__))


def get_config_file_path(config_name):
    return os.path.join(current_directory, 'configs', config_name + '.' + event_config.EventConfiguration.config_format)


class TestEventConfigExistence:
    def test_event_config_does_not_exist(self):
        with pytest.raises(event_config.EventConfigFileDoesNotExistException):
            ec = event_config.EventConfiguration(file_path='pfdkgopdfkg')

    def test_event_config_does_exist(self):
        ec = event_config.EventConfiguration(file_path=get_config_file_path('valid_config'))
        assert ec.config_exists() is True


class TestEventConfigFormatting:
    def test_empty_event_config(self):
        ec = event_config.EventConfiguration(file_path=get_config_file_path('empty_config'))
        with pytest.raises(event_config.InvalidEventConfigException):
            ec.read_config()

    def test_invalid_formatted_event_config(self):
        ec = event_config.EventConfiguration(file_path=get_config_file_path('invalid_json_config'))
        with pytest.raises(event_config.InvalidEventConfigException):
            ec.read_config()

    def test_valid_formatted_but_invalid_content_event_config(self):
        ec = event_config.EventConfiguration(file_path=get_config_file_path('invalid_config'))
        with pytest.raises(event_config.InvalidEventConfigException):
            ec.read_config()


class TestEventConfigAccess:
    def test_event_config_read_time_changing(self):
        ec = event_config.EventConfiguration(file_path=get_config_file_path('valid_config'))
        ec.read_config()
        first_read_time = ec.get_config_last_read_time()
        assert not first_read_time == 0
        sleep(0.25)
        ec.read_config()
        second_read_time = ec.get_config_last_read_time()
        assert not first_read_time == second_read_time

    def test_retrieving_non_existent_config_field_throws_exception(self):
        ec = event_config.EventConfiguration(file_path=get_config_file_path('valid_config'))
        with pytest.raises(event_config.EventConfigFieldDoesNotExistException):
            ec.get_config_value(value_name='test')

    def test_retrieving_integer_when_requesting_number_key_values(self):
        ec = event_config.EventConfiguration(file_path=get_config_file_path('valid_config'))
        values = []
        for key in ec.number_keys:
            values.append(ec.get_config_value(value_name=key))
        for value in values:
            assert isinstance(value, int)

    def test_retrieving_non_integer_when_requesting_non_number_key_values(self):
        ec = event_config.EventConfiguration(file_path=get_config_file_path('valid_config'))
        values = []
        all_keys = ec.keys_required
        non_number_keys = [key for key in all_keys if key not in ec.number_keys]
        for key in non_number_keys:
            values.append(ec.get_config_value(value_name=key))
        for value in values:
            assert not isinstance(value, int)


class TestEventConfigRetrieve:
    def test_no_defined_sources_throwing_invalid_config_exception(self):
        ec = event_config.EventConfiguration(file_path=get_config_file_path('empty_source_event_config'))
        with pytest.raises(event_config.InvalidEventConfigException):
            ec.read_config()

    def test_retrieving_list_when_requesting_lift_key_values(self):
        ec = event_config.EventConfiguration(file_path=get_config_file_path('valid_config'))
        values = []
        for key in ec.list_keys:
            values.append(ec.get_config_value(value_name=key))
        for value in values:
            assert isinstance(value, list)

    def test_end_time_smaller_or_equal_to_start_time_rasies_exception(self):
        ec = event_config.EventConfiguration(file_path=get_config_file_path('invalid_time_config'))
        with pytest.raises(event_config.InvalidEventConfigException):
            ec.read_config()
