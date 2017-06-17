import argparse

import sys

import subprocess
from time import sleep
from urllib.parse import urljoin

import requests
from gevent.pywsgi import WSGIServer


class Service:
    def __init__(self, name, app, address, port, debug):
        self._name = name
        self._app = app
        self._address = address
        self._port = port
        self._debug = debug
        self._http_server = WSGIServer((self._address, self._port), self._app) if not self._debug else None

    @property
    def name(self):
        return self._name

    @property
    def address(self):
        return self._address

    @property
    def port(self):
        return self._port

    @property
    def debug(self):
        return self._debug

    @property
    def http_server(self):
        return self._http_server

    @property
    def full_url(self):
        return 'http://{}:{}/'.format(self._address, self._port)

    @staticmethod
    def create_from_args(name, app, cli_args):
        return Service(
            name=name,
            app=app,
            address=cli_args.address,
            port=cli_args.port,
            debug=cli_args.debug)

    # TODO: Reevaluate why we pass app as a parameter if the service runner does not even use it
    # def start(self):
    #     if self._debug:
    #         self._app.run(host=self._address, port=self._port, debug=self._debug, threaded=True)
    #     else:
    #         self._http_server.serve_forever()
    #
    # def stop(self):
    #     if not self._debug:
    #         self._http_server.stop()

    def create_service_argument_parser(self):
        parser = argparse.ArgumentParser(description=self._name)
        parser.add_argument(
            '-address',
            action='store',
            dest='address',
            default='127.0.0.1',
            help='Address the service will be reachable at')
        parser.add_argument(
            '-port',
            action='store',
            dest='port',
            type=int,
            help='Port the service will use')
        parser.add_argument(
            '--debug',
            dest='debug',
            action='store_true',
            default=False,
            help='Run {} in debug mode'.format(self._name))
        return parser


class ServiceRunner:
    def __init__(self, service, file_path, start_delay=2, stop_delay=2):
        self._service = service
        self._file_path = file_path
        self._process = None
        self._start_delay = start_delay
        self._stop_delay = stop_delay

    def run(self):
        print('Running Service: {} from path: {}'.format(self._service.name, self._file_path))
        args = [
            sys.executable,
            self._file_path,
            '-address',
            self._service.address,
            '-port',
            str(self._service.port)
        ]
        if self._service.debug:
            args.append('--debug')
        self._process = subprocess.Popen(args)
        sleep(self._start_delay)

    def stop_running(self):
        print('Stopping Service: {}'.format(self._service.name))
        self.__destroy_process()
        self._process.kill()

    def __destroy_process(self):
        url = urljoin(self._service.full_url, '/destroy/')
        print('Destroying process for service: {}'.format(self._service.name))
        response = requests.get(url)
        if not response.status_code == 200:
            print(response.status_code)
            print(response.content)
        assert 200 == response.status_code
        sleep(1)
        # TODO: Add check for system OS. This assumes windows
        subprocess.call(['taskkill', '/F', '/T', '/PID', str(self._process.pid)])
        sleep(self._stop_delay)

