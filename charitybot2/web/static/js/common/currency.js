function drawCurrencySymbolOnPage() {
    getCurrencySymbol().then((symbol) => {
        var currencies = document.getElementsByClassName('currency');
        for (var i = 0; i < currencies.length; i++) {
            currencies[i].innerHTML = symbol;
        }
    }).catch((error) => {
        console.error('Unable to get currency symbol: ' + error);
    });
}

function getCurrencySymbol() {
    return new Promise((resolve, reject) => {
        getCurrencyData().then((data) => {
            resolve(convertKeyToCurrency(data['currency_key']));
        }).catch((error) => {
            reject(error);
        });
    });
}

function getCurrencyData() {
    return new Promise((resolve, reject) => {
        fetchJSONFile(
            eventUrl,
            (data) => {
                resolve(data);
            },
            () => {
                reject('Unable to connect to retrieve currency');
            }
        );
    });
}

function convertKeyToCurrency(currencyKey) {
    if (currencyKey == 'EUR') {
        return '€';
    } else if (currencyKey == 'USD') {
        return '$';
    }
    return '£';
}

