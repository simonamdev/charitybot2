// Reference:
// https://stackoverflow.com/questions/14388452/how-do-i-load-a-json-object-from-a-file-with-ajax
function fetchJSONFile(path, callback) {
    var httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function() {
        if (httpRequest.readyState === 4) {
            if (httpRequest.status === 200) {
                var text = httpRequest.responseText;
                var data = JSON.parse(text);
                if (callback) {
                    callback(data);
                }
            }
        }
    };
    httpRequest.open('GET', path);
    httpRequest.send();
}

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
    fetchJSONFile(eventUrl, (data) => {
        console.log(data);
        var header = document.getElementById('overlay-currency');
        header.innerHTML = getCurrencySymbol(data['currency_key']);
    });
}

function getTotal() {
    console.log('Getting Total');
    fetchJSONFile(totalUrl, (data) => {
        console.log(data);
        var header = document.getElementById('overlay-amount');
        header.innerHTML = data['total'];
    });
}

getCurrency();
getTotal();
var updateDelay = 2000; // ms
setInterval(getTotal, updateDelay)