import argparse

from flask import Flask, jsonify
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

private_api_address = '127.0.0.1'
private_api_port = 8001
private_api_url = 'http://{}'.format(private_api_address)
private_api_full_url = '{}:{}/'.format(private_api_url, private_api_port)
private_api_version = 1

debug_mode = False
http_server = WSGIServer((private_api_address, private_api_port), app)


@app.route('/')
@app.route('/api/')
@app.route('/api/v1/')
def index():
    return jsonify(
        {
            'identity': 'CB2 Private API',
            'version': private_api_version
        }
    )


@app.route('/destroy/')
def destroy():
    global debug_mode
    if debug_mode:
        stop_api()
        return 'Shutting down API'
    return 'Debug mode is disables - shutting down is unavailable'


def create_api_process_parser():
    parser = argparse.ArgumentParser(description='CB2 Private API')
    parser.add_argument('--debug', dest='debug', help='Run CB2 Private API in debug mode', action='store_true')
    return parser


def start_api(args):
    global debug_mode
    debug_mode = args.debug
    global http_server
    http_server.serve_forever()


def stop_api():
    global http_server
    http_server.stop()

if __name__ == '__main__':
    cli_args = create_api_process_parser().parse_args(['--debug'])
    start_api(args=cli_args)
