import os

current_directory = os.path.dirname(__file__)
root_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
data_folder = os.path.join(current_directory, 'data')
config_folder = os.path.join(data_folder, 'config')
twitch_config_folder = os.path.join(config_folder, 'twitch')
event_config_folder = os.path.join(config_folder, 'event')
db_folder = os.path.join(data_folder, 'db')
test_folder = os.path.join(root_directory, 'tests')
test_data_folder = os.path.join(test_folder, 'data')
test_config_folder = os.path.join(test_data_folder, 'config')

# Production Configs
purrcat259_config_path = os.path.join(twitch_config_folder, 'purrcat259.json')

# Databases
production_logs_db_path = os.path.join(db_folder, 'logs.db')
production_repository_db_path = os.path.join(db_folder, 'repository.db')

# Script paths
mocksite_path = os.path.join(current_directory, 'sources', 'mocks', 'mocksite.py')
external_api_cli_path = os.path.join(root_directory, 'api.py')
external_api_script_path = os.path.join(current_directory, 'reporter', 'external_api', 'external_api.py')

# Other file paths
status_console_file_path = os.path.join(current_directory, 'reporter', 'status_console', 'console.html')
user_agents_file_path = os.path.join(current_directory, 'sources', 'user_agents.txt')
empty_justgiving_api_key_path = os.path.join(config_folder, 'api', 'empty_justgiving_api_key.txt')
cb2_justgiving_api_key_path = os.path.join(config_folder, 'api', 'cb2_justgiving_api_key.txt')

# Test file paths
debug_justgiving_api_key_path = os.path.join(test_config_folder, 'api', 'debug_justgiving_api_key.txt')
