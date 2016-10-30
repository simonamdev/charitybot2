from charitybot2.paths import production_donations_db_path
from charitybot2.storage.db_handler import DBHandler
from flask import Flask, request, json, render_template
from tests.tests import TestFilePath

app = Flask(__name__)

service_address = '127.0.0.1'
service_port = 9000
service_url = 'http://' + service_address
service_full_url = service_url + ':' + str(service_port) + '/'
service_debug_mode = False

db_handler = DBHandler(donations_db_path=production_donations_db_path)
donations_db = db_handler.get_donations_db()


def parse_request(req):
    return json.loads(req.data.decode('utf-8'))


@app.route('/')
def index():
    return render_template('index.html', event_names=donations_db.get_event_names())


@app.route('/debug')
def debug():
    donations_db_test_path = TestFilePath().get_db_path('donations.db')
    global db_handler
    global donations_db
    db_handler = DBHandler(donations_db_path=donations_db_test_path)
    donations_db = db_handler.get_donations_db()
    return 'Entered debug mode'


@app.route('/identity')
def identity():
    return 'Status Service'


@app.route('/event/<event_name>')
def event(event_name):
    event_data = {
        'name': event_name,
        'donation_count': len(donations_db.get_all_donations(event_name=event_name))
    }
    return render_template('event.html', event_data=event_data)


@app.route('/destroy')
def destroy():
    shutdown_service()
    return 'Shutting down service'


def start_service():
    app.run(host=service_address, port=service_port, debug=True)


def shutdown_service():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


if __name__ == '__main__':
    start_service()