import json
import os

from charitybot2.storage.logs_db import LogsDB
from flask import Flask, request, jsonify


app = Flask(__name__)

service_url = '127.0.0.1'
service_port = 9000
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db', 'logs.db')


def return_db_connection(event_name):
    return LogsDB(db_path=db_path, event_name=event_name)


def check_db_connection():
    try:
        return_db_connection(event_name='test')
        return True
    except Exception as e:
        print(e)
        return False


@app.route('/')
def index():
    return 'Logging Service'


@app.route('/debug', methods=['POST'])
def debug_mode():
    debug_db_path = json.loads(request.data.decode('utf-8'))['db_path']
    if not os.path.isfile(debug_db_path):
        return 'Could not enter debug mode'
    global db_path
    db_path = debug_db_path
    return 'Successfully entered debug mode'


@app.route('/health')
def health():
    health_info = {
        'db': check_db_connection()
    }
    return jsonify(health_info)


@app.route('/log', methods=['POST'])
def log():
    print(request)
    db = return_db_connection(event_name=request.event)
    db.create_log_source_table(log_source=request.source)
    db.log(source=request.source, level=request.level, message=request.message)


@app.route('/destroy')
def destroy():
    shutdown_server()
    return 'Shutting down service'


def start_service():
    app.run(host=service_url, port=service_port, debug=True)


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


if __name__ == '__main__':
    start_service()
