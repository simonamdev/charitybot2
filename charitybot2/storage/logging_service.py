import json

from flask import Flask, request, jsonify

from charitybot2.storage.logs_db import LogsDB


app = Flask(__name__)

service_url = '127.0.0.1'
service_port = 9000


def return_db_connection(event_name):
    return LogsDB(db_path='db/logs.db', event_name=event_name)


def check_db_connection():
    try:
        return_db_connection(event_name='test')
        return True
    except Exception:
        return False


@app.route('/')
def index():
    return 'Logging Service'


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

if __name__ == '__main__':
    app.run(host=service_url, port=service_port, debug=True)
