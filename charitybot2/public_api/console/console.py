from charitybot2.start_service import Service
from flask import Flask
from flask import render_template

app = Flask(__name__)

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
def event(event_identifier):
    return render_template('event.html', event_identifier=event_identifier)


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
