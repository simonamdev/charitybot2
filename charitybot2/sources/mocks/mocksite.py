from flask import Flask, request
app = Flask(__name__)

mocksite_url = '127.0.0.1'
mocksite_port = 5000
mocksite_full_url = 'http://' + mocksite_url + ':' + str(mocksite_port) + '/'

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
    app.run(host=mocksite_url, port=mocksite_port, debug=True)


def shutdown_service():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


if __name__ == '__main__':
    start_service()
