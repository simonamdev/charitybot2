import argparse
import os
import time

from charitybot2.botconfig.event_config import EventConfiguration
from charitybot2.botconfig.json_config import ConfigurationFileDoesNotExistException
from charitybot2.events.currency import Currency
from charitybot2.paths import production_donations_db_path, event_config_folder
from charitybot2.storage.donations_db import DonationsDB
from flask import Flask, request, jsonify, make_response, abort
from flask import render_template
from flask_cors import CORS
from tests.tests import TestFilePath

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
test_donations_db_path = TestFilePath().get_db_path('donations.db')

api_address = '127.0.0.1'
api_port = 8000
api_url = 'http://' + api_address
api_full_url = api_url + ':' + str(api_port) + '/'
debug_mode = False
cli_debug_mode = False

api_paths = {
    'api': {
        'v1': [
            'events',
            'event/:event_name',
            'event/:event_name/donations',
            'event/:event_name/donations?limit=:limit',
            'event/:event_name/donations/last',
            'event/:event_name/donations/distribution'
        ]
    },
    'stats': [
        ':event_name'
    ],
    'overlay': [
        ':event_name'
    ]
}

donations_db = DonationsDB(db_path=test_donations_db_path, debug=True)


def get_currency_symbol(currency_key):
    return Currency(key=currency_key).get_symbol()


def get_event_config(event_name):
    file_path = os.path.join(event_config_folder, event_name + '.json')
    if debug_mode:
        file_path = TestFilePath().get_config_path('event', event_name + '.json')
    event_config = None
    try:
        event_config = EventConfiguration(file_path=file_path)
    except ConfigurationFileDoesNotExistException:
        abort(400)
    return event_config


def get_event_config_value(event_name, key_required):
    return get_event_config(event_name=event_name).get_value(key_name=key_required)


def get_event_config_values(event_name, keys_required=()):
    event_config = get_event_config(event_name=event_name)
    return_values = []
    for key in keys_required:
        return_values.append(event_config.get_value(key_name=key))
    return return_values


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Configuration file missing'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/api/v1/', methods=['GET'])
def index():
    return jsonify(
        {
            'paths': api_paths,
            'debug_allowed': cli_debug_mode,
            'debug': debug_mode
        })


@app.route('/api/v1/events', methods=['GET'])
def events():
    event_names = donations_db.get_event_names()
    if len(event_names) == 0:
        abort(404)
    return jsonify(events=event_names)


@app.route('/api/v1/event/<event_name>', methods=['GET'])
def event_details(event_name):
    if event_name not in donations_db.get_event_names():
        abort(404)
    all_donations = donations_db.get_all_donations(event_name=event_name)
    start_time, end_time, currency_key, target_amount = get_event_config_values(
        event_name=event_name,
        keys_required=('start_time', 'end_time', 'currency', 'target_amount'))
    event_data = {
        'name': event_name,
        'currency_symbol': get_currency_symbol(currency_key=currency_key),
        'start_time': start_time,
        'end_time': end_time,
        'amount_raised': all_donations[-1].get_new_amount(),
        'target_amount': target_amount
    }
    return jsonify(event_data)


@app.route('/api/v1/event/<event_name>/donations')
def event_donations(event_name):
    if not donations_db.event_exists(event_name=event_name):
        abort(404)
    all_donations = donations_db.get_all_donations(event_name=event_name)
    # TODO: Add option to limit via Neopysqlite and not slicing after the fact
    limit = request.args.get('limit')
    if limit is not None:
        all_donations = all_donations[-int(limit):]
    donation_objects = [
        {
            'amount': donation.get_donation_amount(),
            'total_raised': donation.get_new_amount(),
            'timestamp': donation.get_timestamp()
        } for donation in all_donations
    ]
    return jsonify(donations=donation_objects)


@app.route('/api/v1/event/<event_name>/donations/info')
def donations_info(event_name):
    if not donations_db.event_exists(event_name=event_name):
        abort(404)
    all_donations = donations_db.get_all_donations(event_name=event_name)
    current_time_minus_an_hour = int(time.time()) - 3600
    # TODO: Do this in the donations DB module, not here!
    last_hour_donation_count = len([donation for donation in all_donations if donation.get_timestamp() > current_time_minus_an_hour])
    donations_info_object = {
        'count': len(all_donations),
        'average': donations_db.get_average_donation(event_name=event_name),  # TODO: Do properly via SQL AVG() function
        'largest': max(donation.get_donation_amount() for donation in all_donations),
        'last_hour_count': last_hour_donation_count,
    }
    return jsonify(donations_info=donations_info_object)


@app.route('/api/v1/event/<event_name>/donations/last')
def last_event_donation(event_name):
    if event_name not in donations_db.get_event_names():
        abort(404)
    last_donation = donations_db.get_last_donation(event_name=event_name)
    return jsonify(
        {
            'amount': last_donation.get_donation_amount(),
            'total_raised': last_donation.get_new_amount(),
            'timestamp': last_donation.get_timestamp()
        }
    )


@app.route('/api/v1/event/<event_name>/donations/distribution')
def event_donations_distribution(event_name):
    if event_name not in donations_db.get_event_names():
        abort(404)
    all_donations = donations_db.get_all_donations(event_name=event_name)
    distribution = {
        '0-9': 0,
        '10-19': 0,
        '20-29': 0,
        '30-39': 0,
        '40-49': 0,
        '50-75': 0,
        '76-99': 0,
        '100-10000': 0
    }
    for donation in all_donations:
        for bound_string, count in distribution.items():
            bounds = bound_string.split('-')
            lower_bound = int(bounds[0])
            upper_bound = int(bounds[1])
            if lower_bound <= donation.get_donation_amount() <= upper_bound:
                distribution[bound_string] += 1
    return jsonify(donations_distribution=distribution)


@app.route('/overlay/<event_name>')
def amount_raised(event_name):
    if not donations_db.event_exists(event_name=event_name):
        return render_template('overlay.html',
                               event_name=event_name,
                               amount_raised='...',
                               currency_symbol='')
    last_donation = donations_db.get_last_donation(event_name=event_name)
    # Remove decimal point and add thousands separators
    pretty_number = format(int(last_donation.get_new_amount()), ',d')
    currency_key = get_event_config_value(event_name=event_name, key_required='currency')
    currency_symbol = get_currency_symbol(currency_key=currency_key)
    return render_template('overlay.html',
                           event_name=event_name,
                           amount_raised=pretty_number,
                           currency_symbol=currency_symbol)


@app.route('/stats/<event_name>', methods=['GET'])
def status_console(event_name):
    if event_name not in donations_db.get_event_names():
        abort(404)
    return render_template('console.html', event_name=event_name, debug_mode=str(debug_mode).lower())


@app.route('/debug')
def debug():
    if cli_debug_mode:
        global debug_mode
        debug_mode = True
        global donations_db
        donations_db = DonationsDB(db_path=test_donations_db_path, debug=debug_mode)
        return 'Entered API debug mode'
    else:
        return 'Entering API debug mode is not allowed'


@app.route('/destroy')
def destroy():
    global debug_mode
    if debug_mode:
        shutdown_service()
        return 'Shutting down service'
    return 'Not in debug mode - shutting down in unavailable'


def create_api_process_parser():
    parser = argparse.ArgumentParser(description='Charitybot API')
    parser.add_argument('--debug', dest='debug', help='Run Charitybot API in debug mode', action='store_true')
    return parser


def start_api(args):
    global cli_debug_mode
    cli_debug_mode = args.debug
    global donations_db
    if cli_debug_mode:
        print('--- Starting in debug mode ---')
        donations_db = DonationsDB(db_path=test_donations_db_path, debug=True)
    else:
        print('--- Starting in production mode ---')
        donations_db = DonationsDB(db_path=production_donations_db_path, debug=True)
    app.run(host=api_address, port=api_port, debug=cli_debug_mode)


def shutdown_service():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

if __name__ == '__main__':
    args = create_api_process_parser().parse_args(['--debug'])
    start_api(args=args)
