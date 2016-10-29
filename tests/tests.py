import os
import subprocess
import sys

from time import sleep

import requests
from neopysqlite.neopysqlite import Neopysqlite


class TestFilePath:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_dir = os.path.join(self.current_dir, 'data')
        self.db_dir = os.path.join(self.base_dir, 'db')
        self.config_dir = os.path.join(self.base_dir, 'config')

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
        db = Neopysqlite(database_name='Test DB', db_path=self.db_path, verbose=True)
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
    def __init__(self, service_name, service_url, service_path, db_path='', sql_path=''):
        super().__init__(db_path=db_path, sql_path=sql_path)
        self.service_url = service_url
        self.service_name = service_name
        self.service_path = service_path
        self.service = None

    def start_service(self):
        print('Starting Microservice')
        print(self.service_path)
        args = [sys.executable, self.service_path]
        self.service = subprocess.Popen(args)
        sleep(2)

    def stop_service(self):
        print('Stopping Microservice')
        try:
            requests.get(self.service_url + 'destroy')
            print('Accessed service destroy URL')
        except Exception:
            print('Service already destroyed')
        sleep(1)
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
