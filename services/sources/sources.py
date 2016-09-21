from justgiving import JustGivingScraper
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/<fundraiser>/amount')
def get_justgiving_amount(fundraiser):
    jg = JustGivingScraper(fundraiser_name=fundraiser, verbose=True)
    return jg.get_source_value(source_name='amount_raised')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9000, debug=True)
