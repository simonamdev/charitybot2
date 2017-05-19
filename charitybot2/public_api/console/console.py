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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/event/<event_identifier>/')
def event(event_identifier):
    return render_template('event.html', event_identifier=event_identifier)


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
    console_service = Service.create_from_args(name=console_identity, app=app, cli_args=cli_args)
    console_service.start()
