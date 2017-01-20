from urllib.parse import urljoin

from flask import Flask, request, redirect, url_for

app = Flask(__name__)

mocksite_url = '127.0.0.1'
mocksite_port = 5000
mocksite_full_url = 'http://' + mocksite_url + ':' + str(mocksite_port)
mock_justgiving_url = urljoin(mocksite_full_url, '/justgiving/')
mock_justgiving_fundraising_url = mock_justgiving_url + 'fundraising'
mock_justgiving_campaign_url = mock_justgiving_url + 'campaign'

justgiving_amount = 100


@app.route('/')
def index():
    return '<!DOCTYPE html>' \
           '<html>' \
           '<body>' \
           'Mocksite Index Page' \
           '</body>' \
           '</html>'


@app.route('/justgiving/fundraising/')
def justgiving():
    return '<span class="statistics-amount-raised theme-highlight-text-font">' \
           '£{}.52' \
           '</span>'.format(justgiving_amount)


@app.route('/justgiving/campaign/')
def justgiving_campaign():
    return '<p class="dna-text-brand-l jg-theme-text TotalDonation__totalRaised___1sUPY">' \
           '£{}.52' \
           '</p>'.format(justgiving_amount)


@app.route('/justgiving/increase/')
def justgiving_increase():
    global justgiving_amount
    justgiving_amount += 50
    return redirect(url_for('justgiving'))


@app.route('/justgiving/reset/')
def justgiving_reset():
    global justgiving_amount
    justgiving_amount = 100
    return ''


@app.route('/useragent')
def user_agent():
    return request.headers.get('User-Agent')


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
