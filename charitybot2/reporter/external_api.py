from charitybot2.paths import production_donations_db_path
from charitybot2.storage.donations_db import DonationsDB
from flask import Flask, request, jsonify, make_response
from tests.tests import TestFilePath

app = Flask(__name__)

api_address = '127.0.0.1'
api_port = 9000
api_url = 'http://' + api_address
api_full_url = api_url + ':' + str(api_port) + '/'

donations_db = DonationsDB(db_path=production_donations_db_path, debug=False)


@app.route('/', methods=['GET'])
def index():
    return jsonify({'paths': ['events']})


# TODO: Enable entering debug mode only when providing some sort of auth
@app.route('/debug')
def debug():
    donations_db_test_path = TestFilePath().get_db_path('donations.db')
    global donations_db
    donations_db = DonationsDB(db_path=donations_db_test_path, debug=False)
    return 'Entered debug mode'


# TODO: Enable destruction only in debug mode
@app.route('/destroy')
def destroy():
    shutdown_service()
    return 'Shutting down service'


def start_service():
    app.run(host=api_address, port=api_port, debug=False)


def shutdown_service():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


if __name__ == '__main__':
    start_service()

