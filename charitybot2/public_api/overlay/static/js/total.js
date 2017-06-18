//var apiUrl = 'https://api.charitybot.net/api/v1/';
apiAddress = apiAddress + '/api/v1';
var eventUrl = apiAddress + '/event/' + eventIdentifier;
var totalUrl = eventUrl + '/total/';

console.log('Connecting to API via: ' + apiAddress);
if (!updateDelay) {
    var updateDelay = 10000; // ms
}

function getTotal() {
    console.log(totalUrl);
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

drawCurrencySymbolOnPage();
getTotal();
setInterval(getTotal, updateDelay)
