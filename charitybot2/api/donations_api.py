from charitybot2.models.donation import Donation, InvalidDonationException
from charitybot2.paths import production_repository_db_path, test_repository_db_path
from charitybot2.services.donations_service import DonationsService
from charitybot2.start_service import Service
from flask import Flask, jsonify, g, request, abort
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
Donations retrieval/registration Route
"""


@app.route('/api/v1/event/<event_identifier>/donations/', methods=['GET', 'POST'])
def retrieve_or_add_event_donations(event_identifier):
    if request.method == 'POST':
        # Attempt to parse the passed donation
        donation_values = request.form
        try:
            donation = Donation.from_dict(donation_values)
        except InvalidDonationException:
            # Throw a 500
            return jsonify(
                {
                    'error': 'Unable to parse Donation values'
                }
            ), 500
        get_donations_service().register_donation(donation=donation)
        return jsonify(
                {
                    'message': 'Donation with reference {} successfully added'.format(donation.internal_reference)
                }
            )
    else:
        lower_bound, upper_bound, limit = request.args.get('lower'), request.args.get('upper'), request.args.get('limit')
        # If only the latest one is requested
        if lower_bound is None and upper_bound is None and limit == 1:
            donations = [get_donations_service().get_latest_donation(event_identifier=event_identifier)]
        else:
            donations = get_donations_service().get_time_bounded_donations(
                event_identifier=event_identifier,
                lower_bound=lower_bound,
                upper_bound=upper_bound,
                limit=limit)
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


"""
Donation count retrieval Route
"""


@app.route('/api/v1/event/<event_identifier>/donations/count/', methods=['GET'])
def retrieve_number_of_event_donations(event_identifier):
    lower_bound, upper_bound = request.args.get('lower'), request.args.get('upper')
    if lower_bound is None and upper_bound is None:
        count = get_donations_service().get_number_of_donations(event_identifier=event_identifier)
    else:
        count = get_donations_service().get_time_bounded_number_of_donations(
            event_identifier=event_identifier,
            lower_bound=0 if lower_bound is None else lower_bound,
            upper_bound=upper_bound)
    return jsonify(
        {
            'count': count,
            'event_identifier': event_identifier,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound
        }
    )


"""
Donation average amount retrieval Route
"""


@app.route('/api/v1/event/<event_identifier>/donations/average/', methods=['GET'])
def retrieve_average_donation_amount(event_identifier):
    return jsonify(
        {
            'amount': get_donations_service().get_average_donation(event_identifier=event_identifier),
            'event_identifier': event_identifier
        }
    )


"""
Donation Distribution retrieval Route
"""


@app.route('/api/v1/event/<event_identifier>/donations/distribution/', methods=['GET'])
def retrieve_donation_distribution(event_identifier):
    distribution = get_donations_service().get_donation_distribution(event_identifier=event_identifier)
    return jsonify(
        {
            'distribution': distribution,
            'event_identifier': event_identifier
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
