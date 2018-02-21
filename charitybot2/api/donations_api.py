from charitybot2.paths import production_repository_db_path, test_repository_db_path
from charitybot2.services.donations_service import DonationsService
from charitybot2.start_service import Service
from flask import Flask, jsonify, g, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app=app)

version = 1
donations_api_identity = 'CB2 Donations Service'

address = '127.0.0.1'
port = 8001
debug_mode = False

donations_api = Service(
    name=donations_api_identity,
    app=app,
    address=address,
    port=port,
    debug=debug_mode)


def get_repository_path():
    # global debug_mode
    path = production_repository_db_path
    if donations_api.debug:
        path = test_repository_db_path
    return path


def get_donations_service():
    donations_service = getattr(g, '_donations_service', None)
    if donations_service is None:
        donations_service = g._donations_service = DonationsService(
            repository_path=get_repository_path())
        donations_service.open_connections()
    return donations_service


@app.teardown_appcontext
def close_connection(exception):
    donations_service = getattr(g, '_donations_service', None)
    if donations_service is not None:
        donations_service.close_connections()


"""
Identity Route
"""


@app.route('/api/v1/')
def index():
    return jsonify(
        {
            'identity': donations_api_identity,
            'version': version,
            'debug': donations_api.debug
        }
    )


"""
Donations retrieval Route
"""


@app.route('/api/v1/event/<event_identifier>/donations/', methods=['GET'])
def retrieve_event_donations(event_identifier):
    lower_bound, upper_bound, limit = request.args.get('lower'), request.args.get('upper'), request.args.get('limit')
    donations = get_donations_service().get_time_bounded_donations(
        event_identifier=event_identifier,
        lower_bound=lower_bound,
        upper_bound=upper_bound)
    # serialise the donations to dictionaries
    donations = [donation.to_dict() for donation in donations]
    return jsonify(
        {
            'donations': donations,
            'event_identifier': event_identifier,
            'limit': limit,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound
        }
    )


@app.route('/destroy/')
def destroy():
    if donations_api.debug:
        stop_api()
        return 'Shutting down API'
    return 'Debug mode is disabled - shutting down is unavailable'


def stop_api():
    donations_api.stop()

if __name__ == '__main__':
    cli_args = donations_api.create_service_argument_parser().parse_args()
    donations_api = Service.create_from_args(name=donations_api_identity, app=app, cli_args=cli_args)
    donations_api.start()
