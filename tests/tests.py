import json
import os
import subprocess
import sys
import requests


from time import sleep
from neopysqlite import neopysqlite


class TestFilePath:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_dir = os.path.join(self.current_dir, 'data')
        self.db_dir = os.path.join(self.base_dir, 'db')
        self.config_dir = os.path.join(self.base_dir, 'config')

    def get_repository_path(self):
        return self.get_db_path('repository.db')

    def get_logs_path(self):
        return self.get_db_path('logs.db')

    def get_db_path(self, file_name):
        return os.path.join(self.db_dir, file_name)

    def get_config_path(self, sub_directory, file_name):
        return os.path.join(self.config_dir, sub_directory, file_name)


class ResetDB:
    def __init__(self, db_path, sql_path):
        self.db_path = db_path
        self.sql_path = sql_path
        if not db_path == '' and not sql_path == '':
            self.reset_db()

    def reset_db(self):
        print('Resetting Test Database')
        db = neopysqlite.Neopysqlite(database_name='Test DB', db_path=self.db_path, verbose=True)
        commands = self.get_reset_sql_script().split(';')
        for command in commands:
            print(command)
            db.execute_sql(command + ';')
        db.commit_changes()

    def get_reset_sql_script(self):
        sql_string = ''
        with open(self.sql_path, 'r') as sql_file:
            for line in sql_file.readlines():
                sql_string += line.strip()
        return sql_string


class ServiceTest(ResetDB):
    def __init__(self, service_name, service_url, service_path, enter_debug=True, extra_args=[], db_path='',
                 sql_path=''):
        super().__init__(db_path=db_path, sql_path=sql_path)
        self.service_url = service_url
        self.service_name = service_name
        self.service_path = service_path
        self.enter_debug = enter_debug
        self.extra_args = extra_args
        self.service = None

    def start_service(self):
        print('Starting Microservice')
        args = [sys.executable, self.service_path]
        args.extend(self.extra_args)
        self.service = subprocess.Popen(args)
        sleep(4)
        if self.enter_debug:
            response = requests.get(self.service_url + 'debug')
            assert 200 == response.status_code
            print('Entered debug mode for microservice')

    def stop_service(self):
        print('Stopping Microservice')
        try:
            requests.get(self.service_url + 'destroy')
            print('Accessed service destroy URL')
        except Exception:
            print('Service already destroyed')
        sleep(2)
        self.kill_process()

    def kill_process(self):
        print('Attempting to kill process')
        # Attempt graceful termination
        pid = self.service.pid
        self.service.terminate()
        # Attempt force termination
        try:
            os.kill(pid, 0)
            self.service.kill()
            print('Process killed Forcefully')
        except Exception:
            print('Process killed gracefully')


class AdjustTestConfig:
    def __init__(self, config_path):
        self.config_path = config_path
        self.data = None
        self.read_data()

    def read_data(self):
        with open(self.config_path, 'r') as config_file:
            self.data = json.loads(config_file.read())

    def change_value(self, key, value):
        self.data[key] = value
        self.write_data()

    def write_data(self):
        with open(self.config_path, 'w') as config_file:
            json.dump(self.data, config_file)
