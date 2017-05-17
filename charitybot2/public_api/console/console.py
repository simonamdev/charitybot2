from flask import Flask
from flask import render_template
from gevent.pywsgi import WSGIServer

app = Flask(__name__)
# TODO: Automate this part
console_address = '127.0.0.1'
console_port = 5000
console_url = 'http://{}'.format(console_address)
console_full_url = '{}:{}/'.format(console_url, console_port)
debug_mode = True
http_server = WSGIServer((console_address, console_port), app)


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


def start_console():
    global http_server
    global debug_mode
    if debug_mode:
        app.run(host=console_address, port=console_port, debug=True)
    else:
        http_server.serve_forever()


def stop_console():
    global http_server
    http_server.stop()


if __name__ == '__main__':
    start_console()
