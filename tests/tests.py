import os
import subprocess
import sys

from time import sleep
from neopysqlite.neopysqlite import Neopysqlite


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

    def get_reset_sql_script(self):
        sql_string = ''
        with open(self.sql_path, 'r') as sql_file:
            for line in sql_file.readlines():
                sql_string += line.strip()
        return sql_string


class ServiceTest(ResetDB):
    def __init__(self, service_name, service_path, db_path='', sql_path=''):
        super().__init__(db_path=db_path, sql_path=sql_path)
        self.service_name = service_name
        self.service_path = service_path
        self.service = None

    def start_service(self):
        print('Starting Microservice')
        args = [sys.executable, self.service_path]
        self.service = subprocess.Popen(args)
        sleep(2)

    def stop_service(self):
        print('Stopping Microservice gracefully')
        # Attempt graceful termination
        pid = self.service.pid
        self.service.terminate()
        # Attempt force termination
        try:
            os.kill(pid, 0)
            self.service.kill()
            print('Killed Forcefully')
        except Exception:
            print('Killed gracefully')
