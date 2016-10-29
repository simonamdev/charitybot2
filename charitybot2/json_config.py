import os


class ConfigurationFileDoesNotExistException(Exception):
    pass


class InvalidConfigurationException(Exception):
    pass


class JSONConfigurationFile:
    def __init__(self, file_path):
        self.file_path = file_path
        self.confirm_config_exists()
        self.config_data = None
        self.read_config()
        self.validate_config_data()

    def confirm_config_exists(self):
        if not self.config_exists():
            raise ConfigurationFileDoesNotExistException

    def config_exists(self):
        return os.path.isfile(self.file_path)

    def validate_config_data(self):
        if self.config_data == '':
            raise InvalidConfigurationException('Configuration File is empty')

    def read_config(self):
        with open(self.file_path, 'r') as config_file:
            self.config_data = config_file.read()
