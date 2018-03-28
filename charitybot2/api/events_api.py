from charitybot2.paths import production_repository_db_path, test_repository_db_path
from charitybot2.services.events_service import EventsService
from charitybot2.start_service import Service
from flask import Flask, jsonify
from flask import g
from flask_cors import CORS

app = Flask(__name__)
CORS(app=app)

version = 2
events_api_identity = 'CB2 Events Service'

address = '127.0.0.1'
port = 8002
debug_mode = False

events_api = Service(
    name=events_api_identity,
    app=app,
    address=address,
    port=port,
    debug=debug_mode)


def get_repository_path():
    # global debug_mode
    path = production_repository_db_path
    if events_api.debug:
        path = test_repository_db_path
    return path


def get_events_service():
    events_service = getattr(g, '_events_service', None)
    if events_service is None:
        events_service = g._donations_service = EventsService(
            repository_path=get_repository_path())
        events_service.open_connections()
    return events_service


@app.teardown_appcontext
def close_connection(exception):
    events_service = getattr(g, '_events_service', None)
    if events_service is not None:
        events_service.close_connections()


"""
Identity Route
"""


@app.route('/api/v2/')
def index():
    return jsonify(
        {
            'identity': events_api_identity,
            'version': version,
            'debug': events_api.debug
        }
    )


@app.route('/api/v2/event/<event_identifier>/exists/', methods=['GET'])
def event_exists(event_identifier):
    exists = get_events_service().event_is_registered(event_identifier=event_identifier)
    return jsonify(
        {
            'event_identifier': event_identifier,
            'exists': exists
        }
    )


@app.route('/api/v2/events/', methods=['GET'])
def event_identifiers():
    identifiers = get_events_service().get_all_event_identifiers()
    return jsonify(
        {
            'identifiers': identifiers
        }
    )


@app.route('/destroy/')
def destroy():
    if events_api.debug:
        stop_api()
        return 'Shutting down API'
    return 'Debug mode is disabled - shutting down is unavailable'


def stop_api():
    events_api.stop()

if __name__ == '__main__':
    cli_args = events_api.create_service_argument_parser().parse_args()
    events_api = Service.create_from_args(name=events_api_identity, app=app, cli_args=cli_args)
    events_api.start()
