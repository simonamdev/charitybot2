import os

from charitybot2 import paths


class MissingRequiredFolderException(Exception):
    pass


class MissingRequiredFileException(Exception):
    pass


class BotStartupValidator:
    def __init__(self, db_directory=paths.db_folder, config_directory=paths.config_folder):
        self.db_directory = db_directory
        self.config_directory = config_directory
        self.confirm_directories_exist()

    def confirm_directories_exist(self):
        if not os.path.isdir(self.config_directory) or not os.path.isdir(self.db_directory):
            raise MissingRequiredFolderException('Either config or DB directories are missing')

    def confirm_config_exists(self, config_type, file_name):
        if not os.path.isfile(os.path.join(self.config_directory, config_type, file_name)):
            raise MissingRequiredFileException

