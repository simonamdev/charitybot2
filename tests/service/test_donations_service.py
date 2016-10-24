import os

from pathlib import Path

from tests.tests import ServiceTest

print('Donations nicroservice URL is: {}'.format(service_full_url))

current_directory = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_directory, 'db', 'logs.db')
sql_reset_path = os.path.join(current_directory, 'db', 'init_logs_db.sql')
# this can definitely do with its own class to create the paths rather than doing them in each test file
service_script_path = os.path.join(str(Path(os.path.dirname(__file__)).parents[1]), 'charitybot2', 'storage', 'logging_service.py')

service_test = ServiceTest('Logging Service', '', service_path=service_script_path, db_path=db_path,
                           sql_path=sql_reset_path)