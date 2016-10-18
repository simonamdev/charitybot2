from flask import Flask
app = Flask(__name__)

amount = 100


@app.route('/justgiving/')
def justgiving():
    global amount
    amount += 50
    return '<span class="statistics-amount-raised theme-highlight-text-font">{}</span>'.format(amount)


@app.route('/reset/')
def justgiving_reset():
    global amount
    amount = 100
    return ''

if __name__ == '__main__':
    app.run()
