import os
from charitybot2.start_service import Service
from flask import Flask, render_template
from flask import request
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)

users_path = os.path.join(os.path.dirname(__file__), 'users.txt')


# A very insecure way of storing passwords, but an easy one for quickly setting up something for http auth
class Users:
    def __init__(self, path):
        self._path = path
        self._users = dict()
        if not os.path.isfile(self._path):
            raise FileNotFoundError('Users file does not exist')
        self.parse_user_file()

    def parse_user_file(self):
        with open(self._path, 'r') as users_file:
            for line in users_file.readlines():
                parts = line.split(' ')
                self._users[parts[0]] = parts[1].strip()
        print('Users found: {}'.format(list(self._users.keys())))

    def user_exists(self, user):
        return user in self._users.keys()

    def get_password(self, user):
        return self._users[user]


console_identity = 'CB2 Donations Console'
console_address = '127.0.0.1'
console_port = 5000
debug_mode = True
console_service = Service(
    name=console_identity,
    app=app,
    address=console_address,
    port=console_port,
    debug=debug_mode)

auth = HTTPBasicAuth()

users = Users(users_path)


@auth.get_password
def get_pw(username):
    if debug_mode:
        return 'charitybot'
    if users.user_exists(user=username):
        password = users.get_password(user=username)
        return password
    return None


def get_api_address():
    api_address = 'http://127.0.0.1:8001'
    if not debug_mode:
        api_address = 'https://api.charitybot.net'
    return api_address


def get_update_delay():
    delay = 2000
    if not debug_mode:
        delay = 10000
    return delay


@app.context_processor
def inject_api_url():
    return dict(
        api_address=get_api_address(),
        update_delay=get_update_delay())


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/event/<event_identifier>/')
# @auth.login_required
def event(event_identifier):
    return render_template('event.html', event_identifier=event_identifier)


@app.route('/donations/<event_identifier>/')
def donations(event_identifier):
    limit = request.args.get('limit')
    limit = 100 if limit is None else limit
    return render_template('donations.html', event_identifier=event_identifier, limit=limit)


@app.route('/stats/<event_identifier>/')
def stats(event_identifier):
    return render_template('stats.html', event_identifier=event_identifier)


@app.route('/destroy/')
def destroy():
    global debug_mode
    if debug_mode:
        stop_console()
        return 'Shutting down Console'
    return 'Debug mode is disabled - shutting down is unavailable'


def stop_console():
    console_service.stop()


if __name__ == '__main__':
    cli_args = console_service.create_service_argument_parser().parse_args()
    debug_mode = cli_args.debug
    console_service = Service.create_from_args(name=console_identity, app=app, cli_args=cli_args)
    console_service.start()
