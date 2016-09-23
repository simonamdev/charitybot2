import os
import json


class EventConfigFileDoesNotExist(Exception):
    pass


class InvalidEventConfiguration(Exception):
    pass


class EventConfiguration:
    def __init__(self, file_path):
        self.file_path = file_path
        if not self.config_exists():
            raise EventConfigFileDoesNotExist
        self.config_data = None

    def config_exists(self):
        return os.path.isfile(self.file_path)

    def read_config(self):
        with open(self.file_path, 'r') as config_file:
            data = config_file.read()
            if data == '':
                raise InvalidEventConfiguration('Event Configuration file is empty')
        try:
            self.config_data = json.loads(data)
        except json.decoder.JSONDecodeError:
            raise InvalidEventConfiguration('Event Configuration file is not valid JSON')
