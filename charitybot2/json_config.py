import os


class ConfigurationFileDoesNotExistException(Exception):
    pass


class JSONConfigurationFile:
    def __init__(self, file_path):
        self.file_path = file_path
        self.confirm_config_exists()

    def confirm_config_exists(self):
        if not self.config_exists():
            raise ConfigurationFileDoesNotExistException

    def config_exists(self):
        return os.path.isfile(self.file_path)
