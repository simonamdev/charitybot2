import os


class EventConfiguration:
    def __init__(self, file_path):
        self.file_path = file_path

    def config_exists(self):
        return os.path.isfile(self.file_path)
