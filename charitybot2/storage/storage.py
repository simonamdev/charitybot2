from neopysqlite.neopysqlite import Neopysqlite
from flask import Flask

app = Flask(__name__)



@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('event/<event_id>')
def get_event_details():
    mockEvent = {
        'name': 'my_event',
        'id': 'ospkfopkpmdiom',

    }


if __name__ == '__main__':
    app.run()
