import os

current_directory = os.path.dirname(__file__)
data_folder = os.path.join(current_directory, 'data')

# Configs
purrcat259_config_path = os.path.join(data_folder, 'purrcat259.json')

# Databases
production_logs_db_path = os.path.join(data_folder, 'logs.db')
production_donations_db_path = os.path.join(data_folder, 'donations.db')

# Services
mocksite_path = os.path.join(current_directory, 'sources', 'mocks', 'mocksite.py')
status_service_path = os.path.join(current_directory, 'reporter', 'status_service', 'status_service.py')
external_api_path = os.path.join(current_directory, 'reporter', 'external_api', 'external_api.py')
