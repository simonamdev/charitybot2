from urllib.parse import urljoin

from flask import Flask, request, redirect, url_for, render_template, Markup, jsonify
from gevent.pywsgi import WSGIServer
from werkzeug.exceptions import abort

app = Flask(__name__)

mocksite_url = '127.0.0.1'
mocksite_port = 5000
mocksite_full_url = 'http://' + mocksite_url + ':' + str(mocksite_port)
mock_justgiving_url = urljoin(mocksite_full_url, '/justgiving/')
mock_justgiving_fundraising_url = mock_justgiving_url + 'fundraising'
mock_justgiving_campaign_url = mock_justgiving_url + 'campaign'
mock_justgiving_api_url = mock_justgiving_url + 'api/'
actual_justgiving_fundraising_url = 'https://www.justgiving.com/fundraising/FrontierDev'
actual_justgiving_campaign_url = 'https://www.justgiving.com/campaigns/charity/specialeffect/gameblast17'
actual_justgiving_api_url = 'https://api.justgiving.com/v1/campaigns/specialeffect/gameblast17'
http_server = WSGIServer((mocksite_url, mocksite_port), app)

justgiving_amount = 100
mydonate_amount = 100


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
    # The 12th script scraped is the script tag that we need
    script_string = '<script></script>'
    amount_script = '<script>' \
                    '{{"campaign":' \
                    '   {{"totalRaisedInPageCurrency":' \
                    '       {{"currency":' \
                    '           {{"symbol": "£"}},' \
                    '         "value": {0}.52' \
                    '       }}' \
                    '   }}' \
                    '}}' \
                    '</script>'.format(justgiving_amount)
    mocksite_script_strings = ''
    for i in range(0, 11):
        mocksite_script_strings += '\n{}'.format(script_string)
    mocksite_script_strings += '\n{}'.format(amount_script)
    return render_template(
        'amount.html',
        amount_html=Markup(amount_html),
        amount_script=Markup(mocksite_script_strings))


@app.route('/justgiving/api/')
def justgiving_api():
    api_key = request.headers.get('x-api-key')
    if not api_key == 'a1b2c3d4':
        abort(403)
    api_return = dict(
        id=0,
        story='string',
        numberOfFundraisersConnected=0,
        target=0,
        totalRaised='{}.52'.format(justgiving_amount),
        totalOffline=0,
        totalDonated='string',
        totalFundraised='string',
        numberOfDirectDonations=0,
        targetPercentage=0,
        charityId=0,
        description='string',
        charityLogoUrl='string',
        currency='string',
        fundraisingEnabled=True,
        causeId=0,
        campaignPageName='string',
        campaignUrl='string',
        errorMessage='string')
    return jsonify(api_return)


@app.route('/mydonate/teams/')
def mydonate_teams():
    amount_html = '<p class="text-bold display-inline-block font-18 margin-0">' \
                  '<span class="text-primary font-20">£{}.52</span>' \
                  '</p>'.format(mydonate_amount)
    return render_template('amount.html', amount_html=Markup(amount_html))


@app.route('/justgiving/increase/')
def justgiving_increase():
    global justgiving_amount
    justgiving_amount += 50
    return redirect(url_for('justgiving'))


@app.route('/mydonate/increase/')
def mydonate_increase():
    global mydonate_amount
    mydonate_amount += 50
    return redirect(url_for('mydonate_teams'))


@app.route('/justgiving/reset/')
def justgiving_reset():
    global justgiving_amount
    justgiving_amount = 100
    return ''


@app.route('/mydonate/reset/')
def mydonate_reset():
    global mydonate_amount
    mydonate_amount = 100
    return ''


@app.route('/useragent')
def user_agent():
    return request.headers.get('User-Agent')


@app.route('/destroy')
def destroy():
    stop_mocksite()
    return 'Shutting down service'


def start_mocksite():
    print('Starting Mocksite')
    global http_server
    http_server.serve_forever()


def stop_mocksite():
    print('Stopping Mocksite')
    global http_server
    http_server.stop()


if __name__ == '__main__':
    start_mocksite()
