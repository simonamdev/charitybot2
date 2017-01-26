import os


class TestFilePath:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_dir = os.path.join(self.current_dir, 'data')
        self.db_dir = os.path.join(self.base_dir, 'db')
        self.config_dir = os.path.join(self.base_dir, 'config')

    def get_repository_db_path(self):
        return self.get_db_path('repository.db')

    def get_logs_path(self):
        return self.get_db_path('logs.db')

    def get_repository_script_path(self):
        return self.get_db_path('init_database.sql')

    def get_db_path(self, file_name):
        return os.path.join(self.db_dir, file_name)

    def get_config_path(self, sub_directory, file_name):
        return os.path.join(self.config_dir, sub_directory, file_name)


def get_test_config_path(folder, file_name):
    return TestFilePath().get_config_path(sub_directory=folder, file_name=file_name)

# Base Config test paths
empty_config_path = get_test_config_path('base', 'empty_config.json')
invalid_config_path = get_test_config_path('base', 'invalid_formatted_config.json')
valid_config_path = get_test_config_path('base', 'valid_config.json')

# Event Config Paths
valid_event_config_path = get_test_config_path('event', 'valid_config.json')
end_to_end_event_config_path = get_test_config_path('event', 'e2e_config.json')

# Database related Paths
repository_db_path = TestFilePath().get_repository_db_path()
repository_db_script_path = TestFilePath().get_repository_script_path()

logs_db_path = TestFilePath().get_logs_path()
logs_script_path = TestFilePath().get_db_path('logs.sql')
