import json
import os

from charitybot2.storage.logs_db import LogsDB
from flask import Flask, request, jsonify, abort


app = Flask(__name__)

service_url = '127.0.0.1'
service_port = 9000
service_full_url = 'http://' + service_url + ':' + str(service_port) + '/'

current_directory = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_directory, 'db', 'logs.db')
log_keys_required = ['event', 'source', 'level', 'message']


def return_db_connection(event_name):
    return LogsDB(db_path=db_path, event_name=event_name, verbose=True)


def parse_request(req):
    return json.loads(req.data.decode('utf-8'))


def check_db_connection():
    try:
        return_db_connection(event_name='test')
        return True
    except Exception as e:
        raise e


@app.route('/')
def index():
    return 'Logging Service'


@app.route('/debug', methods=['POST'])
def debug_mode():
    debug_db_path = parse_request(request)['db_path']
    if not os.path.isfile(debug_db_path):
        return 'Could not enter debug mode'
    global db_path
    db_path = debug_db_path
    return 'Successfully entered debug mode'


@app.route('/db')
def current_db_path():
    global db_path
    return db_path


@app.route('/health')
def health():
    health_info = {
        'db': check_db_connection()
    }
    return jsonify(health_info)


@app.route('/log', methods=['POST'])
def log():
    request_data = parse_request(request)
    if not sorted(log_keys_required) == sorted(list(request_data.keys())):
        print('Missing keys in log request - returning 500')
        abort(500)
    if list(request_data.values()) == ['', '', '', '']:
        return 'Empty Log passed'
    print(request_data)
    db = return_db_connection(event_name=request_data['event'])
    db.create_log_source_table(log_source=request_data['source'])
    db.log(source=request_data['source'], level=request_data['level'], message=request_data['message'])
    return 'Logging successful'


@app.route('/destroy')
def destroy():
    shutdown_service()
    return 'Shutting down service'


def start_service():
    app.run(host=service_url, port=service_port, debug=True)


def shutdown_service():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


if __name__ == '__main__':
    start_service()
