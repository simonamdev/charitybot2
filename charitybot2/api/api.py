from charitybot2.creators.event_configuration_creator import EventConfigurationCreator
from charitybot2.creators.event_creator import EventRegister
from charitybot2.models.donation import InvalidDonationException, Donation
from charitybot2.paths import production_repository_db_path, test_repository_db_path
from charitybot2.persistence.donation_sqlite_repository import DonationSQLiteRepository
from charitybot2.persistence.event_sqlite_repository import EventSQLiteRepository
from charitybot2.persistence.heartbeat_sqlite_repository import HeartbeatSQLiteRepository
from charitybot2.persistence.sqlite_repository import InvalidRepositoryQueryException
from charitybot2.start_service import Service
from flask import Flask, jsonify, g, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app=app)

private_api_version = 1
private_api_identity = 'CB2 Private API'

# Defaults
private_api_address = '127.0.0.1'
private_api_port = 8001
debug_mode = False
private_api_service = Service(
    name=private_api_identity,
    app=app,
    address=private_api_address,
    port=private_api_port,
    debug=debug_mode)


def get_repository_path():
    # global debug_mode
    path = production_repository_db_path
    if private_api_service.debug:
        path = test_repository_db_path
    return path

event_repository = EventSQLiteRepository(db_path=get_repository_path())
donation_repository = DonationSQLiteRepository(db_path=get_repository_path())
heartbeat_repository = HeartbeatSQLiteRepository(db_path=get_repository_path())


def convert_imdict_to_event_config(imdict):
    actual_dict = imdict.to_dict()
    number_keys = EventConfigurationCreator.number_keys
    for key in number_keys:
        actual_dict[key] = int(actual_dict[key])
    return actual_dict


def get_event_repository():
    event_repo = getattr(g, '_event_repository', None)
    if event_repo is None:
        event_repo = g._event_repository = EventSQLiteRepository(
            db_path=get_repository_path())
    return event_repo


def get_heartbeat_repository():
    heartbeat_repo = getattr(g, '_heartbeat_repository', None)
    if heartbeat_repo is None:
        heartbeat_repo = g._heartbeat_repository = HeartbeatSQLiteRepository(
            db_path=get_repository_path())
    return heartbeat_repo


def get_donations_repository():
    donation_repo = getattr(g, '_donation_repository', None)
    if donation_repo is None:
        donation_repo = g._donation_repository = DonationSQLiteRepository(
            db_path=get_repository_path())
    return donation_repo


@app.teardown_appcontext
def close_connection(exception):
    event_repo = getattr(g, '_event_repository', None)
    if event_repo is not None:
        event_repo.close_connection()
    donation_repo = getattr(g, '_donation_repository', None)
    if donation_repo is not None:
        donation_repo.close_connection()
    heartbeat_repo = getattr(g, '_heartbeat_repository', None)
    if heartbeat_repo is not None:
        heartbeat_repo.close_connection()


@app.route('/')
@app.route('/api/')
@app.route('/api/v1/')
def index():
    return jsonify(
        {
            'identity': private_api_identity,
            'version': private_api_version,
            'debug': private_api_service.debug
        }
    )


@app.route('/api/v1/events')
def all_events():
    event_configurations = get_event_repository().get_events()
    return jsonify(
        {
            'events': [config.configuration_values for config in event_configurations]
        }
    )


@app.route('/api/v1/event/<event_identifier>')
def event_info(event_identifier):
    if not get_event_repository().event_already_registered(identifier=event_identifier):
        return jsonify(
            {
                'message': 'Event not registered'
            }
        )
    event_data = get_event_repository().get_event_configuration(identifier=event_identifier)
    return jsonify(event_data.configuration_values)


@app.route('/api/v1/event/exists/<event_identifier>/')
def event_existence(event_identifier):
    event_exists = get_event_repository().event_already_registered(identifier=event_identifier)
    return jsonify(
        {
            'event_exists': event_exists
        }
    )


@app.route('/api/v1/event/', methods=['POST'])
def register_or_update_event():
    event_register = EventRegister(
        event_configuration=EventConfigurationCreator(
            configuration_values=convert_imdict_to_event_config(request.form)).configuration,
        event_repository=get_event_repository())
    already_registered = event_register.event_is_registered()
    event_register.get_event()
    update_successful = event_register.event_is_registered() and already_registered
    return jsonify(
        {
            'registration_successful': event_register.event_is_registered(),
            'update_successful': update_successful
        }
    )


@app.route('/api/v1/event/<event_identifier>/donations/', methods=['GET'])
def retrieve_event_donations(event_identifier):
    # TODO: Refactor donations repository to use a generic function which can take any number of filters on top
    # Rather than slicing and dicing here. Getting 1000 donations only to return 5 is very inefficient
    def reduce_to_limit(donation_list, limit):
        if limit is None or isinstance(donation_list, Donation):
            return donation_list
        limit = int(limit)
        return donation_list[:limit] if len(donation_list) > limit else donation_list
    lower_bound, upper_bound, limit = request.args.get('lower'), request.args.get('upper'), request.args.get('limit')
    if lower_bound is not None and upper_bound is not None:
        donations = get_donations_repository().get_time_filtered_event_donations(
            event_identifier=event_identifier,
            lower_bound=lower_bound,
            upper_bound=upper_bound)
        donations = reduce_to_limit(donation_list=donations, limit=limit)
    elif limit is not None and int(limit) == 1:
        donations = get_donations_repository().get_latest_event_donation(event_identifier=event_identifier)
    else:
        donations = get_donations_repository().get_event_donations(event_identifier=event_identifier)
        donations = reduce_to_limit(donation_list=donations, limit=limit)
    if isinstance(donations, list):
        donations = [donation.to_json() for donation in donations]
    else:
        donations = donations.to_json()
    return jsonify(
        {
            'donations': donations,
            'limit': limit,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound
        }
    )


@app.route('/api/v1/event/<event_identifier>/donations/largest', methods=['GET'])
def retrieve_largest_event_donation(event_identifier):
    largest_donation = get_donations_repository().get_largest_donation(event_identifier=event_identifier)
    return largest_donation.to_json()


@app.route('/api/v1/event/<event_identifier>/donations/average', methods=['GET'])
def retrieve_average_event_donation_amount(event_identifier):
    average_donation_amount = get_donations_repository().get_average_donation_amount(event_identifier=event_identifier)
    return jsonify(
        {
            'average_donation_amount': average_donation_amount
        }
    )


@app.route('/api/v1/event/<event_identifier>/donations/distribution', methods=['GET'])
def retrieve_event_donation_distribution(event_identifier):
    donation_distribution = get_donations_repository().get_donation_distribution(event_identifier=event_identifier)
    return jsonify(
        {
            'distribution': donation_distribution
        }
    )


@app.route('/api/v1/event/<event_identifier>/donations/count', methods=['GET'])
def retrieve_event_donation_count(event_identifier):
    lower_bound, upper_bound = request.args.get('lower'), request.args.get('upper')
    count = None
    if lower_bound is not None and upper_bound is not None:
        count = get_donations_repository().get_donation_count(
            event_identifier=event_identifier,
            time_lower_bound=int(lower_bound),
            time_upper_bound=int(upper_bound))
    else:
        count = get_donations_repository().get_donation_count(event_identifier=event_identifier)
    return jsonify(
        {
            'count': count
        }
    )


@app.route('/api/v1/event/<event_identifier>/total/', methods=['GET'])
def retrieve_event_total(event_identifier):
    amount = get_event_repository().get_event_current_amount(identifier=event_identifier)
    return jsonify(
        {
            'total': round(amount, 2)
        }
    )


@app.route('/api/v1/heartbeat/', methods=['POST'])
def heartbeat():
    received_data = request.form.to_dict()
    success = True
    try:
        get_heartbeat_repository().store_heartbeat(
            source=received_data['source'],
            state=received_data['state'],
            timestamp=int(received_data['timestamp']))
    except InvalidRepositoryQueryException:
        success = False
    return jsonify(
        {
            'received': success
        }
    )


@app.route('/api/v1/donation/', methods=['POST'])
def record_donation():
    success = False
    message = 'Donation successfully added'
    received_data = {}
    try:
        received_data = request.form.to_dict()
        new_donation = Donation.from_dict(received_data)
        get_donations_repository().record_donation(new_donation)
        success = True
    except InvalidRepositoryQueryException as e:
        message = 'Donation Repository Error: {}'.format(e)
    except InvalidDonationException as e:
        message = 'Donation was invalid: {}'.format(e)
        print('Error: {} Data: {}'.format(e, received_data))
    except Exception as e:
        message = 'Unknown exception: {}'.format(e)
    return jsonify(
        {
            'received': success,
            'message': message
        }
    )


@app.route('/destroy/')
def destroy():
    if private_api_service.debug:
        stop_api()
        return 'Shutting down API'
    return 'Debug mode is disabled - shutting down is unavailable'


def stop_api():
    private_api_service.stop()

if __name__ == '__main__':
    cli_args = private_api_service.create_service_argument_parser().parse_args()
    private_api_service = Service.create_from_args(name=private_api_identity, app=app, cli_args=cli_args)
    private_api_service.start()
