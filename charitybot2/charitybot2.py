import os


class MissingRequiredFolderException(Exception):
    pass


class BotStartupValidator:
    def __init__(self, db_directory, config_directory):
        self.db_directory = db_directory
        self.config_directory = config_directory
        self.confirm_directories_exist()

    def confirm_directories_exist(self):
        if not os.path.isdir(self.config_directory) or not os.path.isdir(self.db_directory):
            raise MissingRequiredFolderException('Either config or DB directories are missing')
