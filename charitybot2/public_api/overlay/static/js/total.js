var apiUrl = 'http://127.0.0.1:8001/api/v1/';
var eventUrl = apiUrl + 'event/' + eventIdentifier;
var totalUrl = eventUrl + '/total/';

function getCurrencySymbol(currencyKey) {
    if (currencyKey == 'EUR') {
        return '€';
    } else if (currencyKey == 'USD') {
        return '$';
    }
    return '£';
}

function getCurrency() {
    fetchJSONFile(
        eventUrl,
        (data) => {
            console.log(data);
            var header = document.getElementById('overlay-currency');
            header.innerHTML = getCurrencySymbol(data['currency_key']);
        },
        () => {
            console.error('Unable to connect to retrieve currency');
        }
    );
}

function getTotal() {
    console.log('Getting Total');
    fetchJSONFile(totalUrl, (data) => {
        console.log(data);
        var header = document.getElementById('overlay-amount');
        header.innerHTML = data['total'];
    }, () => {
        markUnavailable();
    });
}

function markUnavailable() {
    var header = document.getElementById('overlay-amount');
    header.innerHTML = 'Unable to connect';
}

getCurrency();
getTotal();
var updateDelay = 2000; // ms
setInterval(getTotal, updateDelay)