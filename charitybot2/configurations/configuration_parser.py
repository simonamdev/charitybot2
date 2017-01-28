import json
import os


class InvalidConfigurationException(Exception):
    pass


class ConfigurationParser:
    def __init__(self, file_path, keys_required):
        self._file_path = file_path
        self._keys_required = keys_required if keys_required is not None else ()
        self._raw_data = None
        self._data = dict()
        self.__retrieve_data()
        self.__validate_configuration()

    def get_value(self, key):
        return self._data[key]

    def __validate_configuration(self):
        self.__validate_file_exists()
        self.__validate_data_is_not_empty()
        self.__validate_data_is_properly_formatted()
        self.__validate_keys_match_required_keys()

    def __validate_file_exists(self):
        if not os.path.isfile(self._file_path):
            raise FileNotFoundError('Configuration file does not exist at the path: {}'.format(self._file_path))

    def __validate_data_is_not_empty(self):
        if self._raw_data == '':
            raise InvalidConfigurationException('Configuration file is empty')

    def __validate_data_is_properly_formatted(self):
        try:
            self._data = json.loads(self._raw_data)
        except json.decoder.JSONDecodeError:
            raise InvalidConfigurationException('Configuration file is not properly formatted')

    def __validate_keys_match_required_keys(self):
        keys_left_over = [key for key in self._data.keys() if key not in self._keys_required]
        if len(keys_left_over) > 0:
            raise InvalidConfigurationException('Configuration file has mismatching keys to those required.'
                                                'Illegal keys: {}'.format(keys_left_over))

    def __retrieve_data(self):
        with open(self._file_path, 'r') as config_file:
            self._raw_data = config_file.read()

    def __key_exists(self, key):
        return key in self._data.keys()
