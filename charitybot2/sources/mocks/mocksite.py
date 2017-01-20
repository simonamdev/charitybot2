from urllib.parse import urljoin

from flask import Flask, request, redirect, url_for, render_template, Markup

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
    return render_template('index.html')


@app.route('/justgiving/fundraising/')
def justgiving():
    amount_html = '<span class="statistics-amount-raised theme-highlight-text-font">' \
                   '£{}.52' \
                   '</span>'.format(justgiving_amount)
    return render_template('amount.html', amount_html=Markup(amount_html))


@app.route('/justgiving/campaign/')
def justgiving_campaign():
    amount_html = '<p id="mock-p" class="dna-text-brand-l jg-theme-text TotalDonation__totalRaised___1sUPY"></p>'
    amount_script = '<script>document.getElementById("mock-p").innerHTML = "£{}.52";</script>'.format(justgiving_amount)
    return render_template(
        'amount.html',
        amount_html=Markup(amount_html),
        amount_script=Markup(amount_script))


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
