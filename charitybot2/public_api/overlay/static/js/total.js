apiAddress = apiAddress + '/api/v1';
var eventUrl = apiAddress + '/event/' + eventIdentifier;
var totalUrl = eventUrl + '/total/';

console.log('Connecting to API via: ' + apiAddress);

function getTotal() {
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
    header.innerHTML = 'Connection error';
}

drawCurrencySymbolOnPage();
getTotal();
setInterval(getTotal, updateDelay)
