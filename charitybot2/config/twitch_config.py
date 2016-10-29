import os


class TwitchAccountConfigurationFileDoesNotExistException(Exception):
    pass


class TwitchAccountConfiguration:
    config_format = 'JSON'

    def __init__(self, file_path):
        self.file_path = file_path
        if not self.config_exists():
            raise TwitchAccountConfigurationFileDoesNotExistException

    def config_exists(self):
        return os.path.isfile(self.file_path)
