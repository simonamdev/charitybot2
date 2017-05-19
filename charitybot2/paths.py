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
test_db_folder = os.path.join(test_data_folder, 'db')
base_test_config_folder = os.path.join(test_config_folder, 'base')
event_test_config_folder = os.path.join(test_config_folder, 'event')

# Production Configs
purrcat259_config_path = os.path.join(twitch_config_folder, 'purrcat259.json')

# Test Configs
empty_test_config_path = os.path.join(base_test_config_folder, 'empty_config.json')
invalid_test_config_path = os.path.join(base_test_config_folder, 'invalid_formatted_config.json')
valid_test_config_path = os.path.join(base_test_config_folder, 'valid_config.json')
valid_test_event_config_path = os.path.join(event_test_config_folder, 'valid_config.json')

# Databases
production_logs_db_path = os.path.join(db_folder, 'logs.db')
production_repository_db_path = os.path.join(db_folder, 'repository.db')
test_repository_db_path = os.path.join(test_db_folder, 'repository.db')

# Script paths
mocksite_path = os.path.join(current_directory, 'sources', 'mocks', 'mocksite.py')
external_api_cli_path = os.path.join(root_directory, 'api.py')
external_api_script_path = os.path.join(current_directory, 'reporter', 'external_api', 'external_api.py')
private_api_script_path = os.path.join(current_directory, 'private_api', 'private_api.py')
console_script_path = os.path.join(current_directory, 'public_api', 'console', 'console.py')
overlay_script_path = os.path.join(current_directory, 'public_api', 'overlay', 'overlay.py')

# SQL Script paths
init_donations_script_path = os.path.join(db_folder, 'init_donations.sql')
init_events_script_path = os.path.join(db_folder, 'init_events.sql')
init_logs_script_path = os.path.join(db_folder, 'init_logs.sql')
init_heartbeat_script_path = os.path.join(db_folder, 'init_heartbeat.sql')
init_test_sql_script_path = os.path.join(db_folder, 'init_test.sql')

# Other file paths
status_console_file_path = os.path.join(current_directory, 'reporter', 'status_console', 'console.html')
user_agents_file_path = os.path.join(current_directory, 'sources', 'user_agents.txt')
empty_justgiving_api_key_path = os.path.join(config_folder, 'api', 'empty_justgiving_api_key.txt')
cb2_justgiving_api_key_path = os.path.join(config_folder, 'api', 'cb2_justgiving_api_key.txt')

# Test file paths
debug_justgiving_api_key_path = os.path.join(test_config_folder, 'api', 'debug_justgiving_api_key.txt')
