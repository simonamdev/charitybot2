import json
import os
import subprocess
import sys
from time import sleep

import requests
from charitybot2.paths import mocksite_path, external_api_cli_path
from charitybot2.reporter.external_api.external_api import api_full_url
from neopysqlite import neopysqlite


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


class WebServer:
    def __init__(self, name, url, script_path, extra_args=(), start_delay=3, stop_delay=2):
        self.name = name
        self.url = url
        self.script_path = script_path
        self.extra_args = extra_args
        self.start_delay = start_delay
        self.stop_delay = stop_delay
        self.web_server = None

    def start(self):
        print('Starting Web Server for: {}'.format(self.name))
        args = [sys.executable, self.script_path]
        args.extend(list(self.extra_args))
        self.web_server = subprocess.Popen(args)
        sleep(self.start_delay)

    def stop(self):
        print('Stopping Web Server for: {}'.format(self.name))
        self.__kill_process()

    def __kill_process(self):
        print('Killing process for: {}'.format(self.name))
        sleep(self.stop_delay)
        pid = self.web_server.pid
        os.kill(pid, 0)
        self.web_server.kill()


class MockFundraisingWebsite(WebServer):
    def __init__(self, fundraiser_name, extra_args=()):
        self.url = 'http://127.0.0.1:5000'
        self.fundraiser_name = fundraiser_name
        super().__init__(
            name='Mock Fundraising Website',
            url=self.url,
            script_path=mocksite_path,
            extra_args=extra_args)

    def reset_amount(self):
        response = requests.get(url=self.url + '/{}/reset/'.format(self.fundraiser_name))
        assert 200 == response.status_code

    def increase_amount(self):
        response = requests.get(url=self.url + '/{}/increase'.format(self.fundraiser_name))
        assert 200 == response.status_code


class MockExternalAPI(WebServer):
    def __init__(self, extra_args=(), enter_debug=True):
        self.url = api_full_url
        self.enter_debug = enter_debug
        super().__init__(
            name='Mock External API',
            url=self.url,
            script_path=external_api_cli_path,
            extra_args=extra_args,
            start_delay=5)

    def start(self):
        super().start()
        if self.enter_debug:
            self.__enter_debug_mode()

    def stop(self):
        self.__destroy_api()
        super().stop()

    def __destroy_api(self):
        response = requests.get(self.url + 'destroy')
        assert 200 == response.status_code

    def __enter_debug_mode(self):
        print('Entering debug mode for: {}'.format(self.name))
        response = requests.get(self.url + 'debug')
        assert 200 == response.status_code
        assert 'Entered API debug mode' == response.content.decode('utf-8')


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
