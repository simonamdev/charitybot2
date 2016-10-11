import os
import json
import time
import collections


class EventConfigFileDoesNotExistException(Exception):
    pass


class InvalidEventConfigException(Exception):
    pass


class EventConfigFieldDoesNotExistException(Exception):
    pass


class EventConfiguration:
    config_format = 'JSON'
    keys_required = [
        'name',
        'start_time',
        'end_time',
        'source_url',
        'update_tick'
    ]

    number_keys = [
        'start_time',
        'end_time',
        'update_tick'
    ]

    list_keys = [
        'sources_required'
    ]

    def __init__(self, file_path):
        self.file_path = file_path
        if not self.config_exists():
            raise EventConfigFileDoesNotExistException
        self.config_data = None
        self.config_read_time = 0
        self.config_is_valid = False

    def config_exists(self):
        return os.path.isfile(self.file_path)

    def read_config(self):
        self.config_read_time = time.time()
        with open(self.file_path, 'r') as config_file:
            data = config_file.read()
            if data == '':
                raise InvalidEventConfigException('Event Configuration file is empty')
        try:
            self.config_data = json.loads(data)
        except json.decoder.JSONDecodeError:
            raise InvalidEventConfigException('Event Configuration file '
                                              'is not correctly formatted {0}'.format(EventConfiguration.config_format))
        self.validate_config_data()

    def get_config_last_read_time(self):
        return self.config_read_time

    def validate_config_data(self):
        current_config_keys = self.config_data.keys()
        same_keys_found = sorted(current_config_keys) == sorted(EventConfiguration.keys_required)
        if not same_keys_found:
            raise InvalidEventConfigException('Event Configuration file is not valid: it has some missing keys')
        if len(self.config_data['sources_required']) == 0:
            raise InvalidEventConfigException('Event Configuration file has no sources defined')
        if self.config_data['end_time'] <= self.config_data['start_time']:
            raise InvalidEventConfigException('Event end time cannot be after or the same as event start time')

    def get_config_value(self, value_name):
        self.read_config()
        if value_name not in EventConfiguration.keys_required:
            raise EventConfigFieldDoesNotExistException('Value {0} does not exist as one of the config fields'.format(value_name))
        return_value = self.config_data[value_name]
        return int(return_value) if value_name in EventConfiguration.number_keys else return_value
