import argparse

from charitybot2.creators.event_configuration_creator import EventConfigurationCreator
from charitybot2.creators.event_creator import EventRegister
from charitybot2.paths import production_repository_db_path
from charitybot2.persistence.event_sqlite_repository import EventSQLiteRepository
from flask import Flask, jsonify, g, request
from gevent.pywsgi import WSGIServer
from tests.paths_for_tests import test_repository_db_path

app = Flask(__name__)

private_api_address = '127.0.0.1'
private_api_port = 8001
private_api_url = 'http://{}'.format(private_api_address)
private_api_full_url = '{}:{}/'.format(private_api_url, private_api_port)
private_api_version = 1

debug_mode = False
http_server = WSGIServer((private_api_address, private_api_port), app)
private_api_identity = 'CB2 Private API'
event_repository = EventSQLiteRepository(db_path=production_repository_db_path, debug=debug_mode)


def convert_imdict_to_event_config(imdict):
    actual_dict = imdict.to_dict()
    number_keys = EventConfigurationCreator.number_keys
    for key in number_keys:
        actual_dict[key] = int(actual_dict[key])
    return actual_dict


def get_repository_path():
    global debug_mode
    path = production_repository_db_path
    if debug_mode:
        path = test_repository_db_path
    return path


def get_event_repository():
    event_repo = getattr(g, '_event_repository', None)
    if event_repo is None:
        event_repo = g._event_repository = EventSQLiteRepository(
            db_path=get_repository_path())
    return event_repo


@app.teardown_appcontext
def close_connection(exception):
    event_repo = getattr(g, '_event_repository', None)
    if event_repo is not None:
        event_repo.close_connection()


@app.route('/')
@app.route('/api/')
@app.route('/api/v1/')
def index():
    return jsonify(
        {
            'identity': private_api_identity,
            'version': private_api_version,
            'debug': debug_mode
        }
    )


@app.route('/api/v1/event/<event_identifier>/')
def event_info(event_identifier):
    event_exists = get_event_repository().event_already_registered(identifier=event_identifier)
    return jsonify(
        {
            'event_exists': event_exists
        }
    )


@app.route('/api/v1/event/register/', methods=['POST'])
def register_event():
    event_register = EventRegister(
        event_configuration=EventConfigurationCreator(
            configuration_values=convert_imdict_to_event_config(request.form)).configuration,
        event_repository=get_event_repository())
    event_register.get_event()
    return jsonify(
        {
            'registration_successful': event_register.event_is_registered()
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
    global event_repository
    event_repository = EventSQLiteRepository(db_path=get_repository_path())
    global http_server
    if debug_mode:
        app.run(host=private_api_address, port=private_api_port, debug=True)
    else:
        http_server.serve_forever()


def stop_api():
    global http_server
    http_server.stop()

if __name__ == '__main__':
    cli_args = create_api_process_parser().parse_args(['--debug'])
    start_api(args=cli_args)
