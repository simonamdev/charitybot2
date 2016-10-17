from flask import Flask
app = Flask(__name__)


@app.route('/justgiving/<amount>')
def justgiving(amount=100):
    return '<span class="statistics-amount-raised theme-highlight-text-font">{}</span>'.format(amount)

if __name__ == '__main__':
    app.run()
