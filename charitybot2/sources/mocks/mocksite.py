from flask import Flask, request
app = Flask(__name__)

service_url = '127.0.0.1'
service_port = 9000
service_full_url = 'http://' + service_url + ':' + str(service_port) + '/'

amount = 100


@app.route('/justgiving/')
def justgiving():
    global amount
    amount += 50
    return '<span class="statistics-amount-raised theme-highlight-text-font">£{}.52</span>'.format(amount)


@app.route('/reset/')
def justgiving_reset():
    global amount
    amount = 100
    return ''


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