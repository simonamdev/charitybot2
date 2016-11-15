from charitybot2.events.currency import Currency
from charitybot2.paths import production_donations_db_path
from charitybot2.storage.donations_db import DonationsDB
from flask import Flask, request, jsonify, make_response, abort
from flask import render_template
from flask_cors import CORS, cross_origin
from tests.tests import TestFilePath

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

api_address = '127.0.0.1'
api_port = 9000
api_url = 'http://' + api_address
api_full_url = api_url + ':' + str(api_port) + '/'
debug_mode = True

api_paths = [
    'events',
    'event/:event_name',
    'event/:event_name/donations',
    'event/:event_name/donations?limit=:limit',
    'event/:event_name/donations/last'
]

donations_db = DonationsDB(db_path=production_donations_db_path, debug=debug_mode)


def get_currency_symbol(event_name):
    return Currency(key=donations_db.get_event_currency_key(event_name=event_name)).get_symbol()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/', methods=['GET'])
def index():
    return jsonify({'paths': api_paths})


@app.route('/events', methods=['GET'])
def events():
    event_names = donations_db.get_event_names()
    if len(event_names) == 0:
        abort(404)
    return jsonify(events=event_names)


@app.route('/event/<event_name>', methods=['GET'])
def event_details(event_name):
    if event_name not in donations_db.get_event_names():
        abort(404)
    all_donations = donations_db.get_all_donations(event_name=event_name)
    event_data = {
        'name': event_name,
        'donation_count': len(all_donations),
        'donation_average': donations_db.get_average_donation(event_name=event_name),
        'largest_donation': max(donation.get_donation_amount() for donation in all_donations),
        'currency_symbol': get_currency_symbol(event_name=event_name)
    }
    return jsonify(event_data)


@app.route('/event/<event_name>/donations')
def event_donations(event_name):
    if event_name not in donations_db.get_event_names():
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


@app.route('/event/<event_name>/donations/last')
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


@app.route('/event/<event_name>/overlay')
def amount_raised(event_name):
    if event_name not in donations_db.get_event_names():
        return render_template('overlay.html',
                               event_name=event_name,
                               amount_raised='ERROR',
                               currency_symbol='')
    last_donation = donations_db.get_last_donation(event_name=event_name)
    return render_template('overlay.html',
                           event_name=event_name,
                           amount_raised=last_donation.get_new_amount(),
                           currency_symbol=get_currency_symbol(event_name=event_name))


# TODO: Enable entering debug mode only when providing some sort of auth
@app.route('/debug')
def debug():
    donations_db_test_path = TestFilePath().get_db_path('donations.db')
    global debug_mode
    debug_mode = True
    global donations_db
    donations_db = DonationsDB(db_path=donations_db_test_path, debug=debug_mode)
    return 'Entered debug mode'


@app.route('/destroy')
def destroy():
    global debug_mode
    if debug_mode:
        shutdown_service()
        return 'Shutting down service'
    return 'Not in debug mode - shutting down in unavailable'


def start_service():
    app.run(host=api_address, port=api_port, debug=debug_mode)


def shutdown_service():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


if __name__ == '__main__':
    start_service()
