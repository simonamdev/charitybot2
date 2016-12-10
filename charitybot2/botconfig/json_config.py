import json
import os


class ConfigurationFileDoesNotExistException(Exception):
    pass


class InvalidConfigurationException(Exception):
    pass


class ConfigurationFieldDoesNotExistException(Exception):
    pass


class JSONConfigurationFile:
    def __init__(self, file_path, keys_required):
        self.file_path = file_path
        self.keys_required = keys_required
        self.confirm_config_exists()
        self.config_raw_data = None
        self.config_data = None
        self.read_config()
        self.validate_config_data()
        self.run_extra_validation()

    def confirm_config_exists(self):
        if not self.config_exists():
            raise ConfigurationFileDoesNotExistException

    def config_exists(self):
        return os.path.isfile(self.file_path)

    def validate_config_data(self):
        self.validate_config_is_not_empty()
        self.validate_config_is_properly_formatted()
        self.validate_config_keys()

    def validate_config_is_not_empty(self):
        if self.config_raw_data == '':
            raise InvalidConfigurationException('Configuration File is empty')

    def validate_config_is_properly_formatted(self):
        try:
            self.config_data = json.loads(self.config_raw_data)
        except json.decoder.JSONDecodeError:
            raise InvalidConfigurationException('Configuration File is not properly formatted JSON')

    def validate_config_keys(self):
        if not sorted(self.config_data.keys()) == sorted(self.keys_required):
            raise InvalidConfigurationException

    def run_extra_validation(self):
        # Override to provide extra validation according to the inheriting config type
        # Such as checking that a URL is not empty and not a number
        pass

    def read_config(self):
        with open(self.file_path, 'r') as config_file:
            self.config_raw_data = config_file.read()

    def get_value(self, key_name):
        if not self.key_exists(key_name=key_name):
            raise ConfigurationFieldDoesNotExistException('The key {} is non-existent'.format(key_name))
        return self.config_data[key_name]

    def key_exists(self, key_name):
        return key_name in self.config_data.keys()
