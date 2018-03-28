from charitybot2.creators.event_configuration_creator import EventConfigurationCreator, \
    InvalidEventConfigurationException
from charitybot2.paths import production_repository_db_path, test_repository_db_path
from charitybot2.services.events_service import EventsService
from charitybot2.start_service import Service
from flask import Flask, jsonify
from flask import g
from flask import request
from flask_cors import CORS

app = Flask(__name__)
CORS(app=app)

version = 2
events_api_identity = 'CB2 Events Service'

address = '127.0.0.1'
port = 8002
debug_mode = False
full_url = 'http://{}/{}/'.format(address, port)

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


"""
Event Existence Route
"""


@app.route('/api/v2/event/<event_identifier>/exists/', methods=['GET'])
def event_existence(event_identifier):
    exists = get_events_service().event_is_registered(event_identifier=event_identifier)
    return jsonify(
        {
            'event_identifier': event_identifier,
            'exists': exists
        }
    )


"""
Event Identifiers Retrieval Route
"""


@app.route('/api/v2/events/', methods=['GET'])
def event_identifiers():
    identifiers = get_events_service().get_all_event_identifiers()
    return jsonify(
        {
            'identifiers': identifiers
        }
    )


"""
Event Info Retrieval and Creation Route
"""


@app.route('/api/v2/event/<event_identifier>/', methods=['GET', 'POST'])
def event_info(event_identifier):
    event_exists = get_events_service().event_is_registered(event_identifier=event_identifier)
    if request.method == 'POST':
        # Attempt to recreate the event configuration from the values
        event_configuration_values = request.form.to_dict()
        try:
            event_configuration = EventConfigurationCreator(
                configuration_values=event_configuration_values).configuration
        except InvalidEventConfigurationException as e:
            # Return 500
            return jsonify(
                {
                    'success': False,
                    'error': str(e)
                }
            ), 500
        # Check if the event exists first, so as to update it rather than create it in that case
        if event_exists:
            # Update the event
            get_events_service().update_event(event_configuration=event_configuration)
        else:
            # Create the event
            get_events_service().register_event(event_configuration=event_configuration)
        return jsonify(
            {
                'event_identifier': event_configuration.identifier,
                'success': True
            }
        )
    else:
        # Check if the event exists first
        if not event_exists:
            return jsonify(
                {
                    'exists': False,
                    'info': {}
                }
            )
        configuration = get_events_service().get_event_configuration(event_identifier=event_identifier)
        return jsonify(
            {
                'exists': True,
                'info': configuration.configuration_values
            }
        )


"""
Event Info Retrieval and Creation Route
"""


@app.route('/api/v2/event/<event_identifier>/update/', methods=['POST'])
def update_event_info(event_identifier):
    event_exists = get_events_service().event_is_registered(event_identifier=event_identifier)
    if not event_exists:
        return jsonify(
            {
                'success': False,
                'error': 'Event with Identifier: {} does not exist'.format(event_identifier)
            }
        ), 500
    # Attempt to recreate the event configuration from the values
    event_configuration_values = request.form.to_dict()
    try:
        event_configuration = EventConfigurationCreator(
            configuration_values=event_configuration_values).configuration
    except InvalidEventConfigurationException as e:
        # Return 500
        return jsonify(
            {
                'success': False,
                'error': str(e)
            }
        ), 500
    # Check if the event exists first, so as to update it rather than create it in that case
    get_events_service().update_event(event_configuration=event_configuration)
    return jsonify(
        {
            'event_identifier': event_configuration.identifier,
            'success': True
        }
    )


"""
Event Total Retrieval Route
"""


@app.route('/api/v2/event/<event_identifier>/total/', methods=['GET', 'POST'])
def event_total(event_identifier):
    exists = get_events_service().event_is_registered(event_identifier=event_identifier)
    if not exists:
        return jsonify(
            {
                'event_identifier': event_identifier,
                'exists': False,
                'total': None
            }
        ), 500
    total = get_events_service().get_event_total(event_identifier=event_identifier)
    # If we are updating the total, then it is a POST request, otherwise we are only retrieving the total
    if request.method == 'POST':
        data = request.form.to_dict()
        try:
            get_events_service().set_event_total(event_identifier=event_identifier, total=float(data['total']))
        except ValueError:
            return jsonify(
                {
                    'event_identifier': event_identifier,
                    'exists': True,
                    'success': False,
                    'error': 'Total value is not of the correct type'
                }
            ), 500
        total = data['total']
    return jsonify(
        {
            'event_identifier': event_identifier,
            'exists': True,
            'success': True,
            'total': total
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
