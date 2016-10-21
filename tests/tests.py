import sys

import subprocess
from time import sleep

from neopysqlite.neopysqlite import Neopysqlite


class ResetDB:
    def __init__(self, db_path, sql_path):
        self.db_path = db_path
        self.sql_path = sql_path
        self.reset_db()

    def reset_db(self):
        db = Neopysqlite(database_name='Test DB', db_path=self.db_path, verbose=True)
        commands = self.get_reset_sql_script().split(';')
        for command in commands:
            db.execute_sql(command + ';')

    def get_reset_sql_script(self):
        sql_string = ''
        with open(self.sql_path, 'r') as sql_file:
            for line in sql_file.readlines():
                sql_string += line.strip()
        return sql_string


class ServiceTest(ResetDB):
    def __init__(self, db_path, sql_path, service_path):
        super().__init__(db_path=db_path, sql_path=sql_path)
        self.service_path = service_path
        self.service = None

    def start_service(self):
        print('Starting Microservice')
        args = [sys.executable, self.service_path]
        self.service = subprocess.Popen(args)
        sleep(2)

    def stop_service(self):
        print('Stopping Microservice')
        self.service.terminate()
