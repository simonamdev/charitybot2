apiAddress = apiAddress + '/api/v1';
var eventUrl = apiAddress + '/event/' + eventIdentifier;
var totalUrl = eventUrl + '/total/';

console.log('Connecting to API via: ' + apiAddress);
var amountElementId = 'overlayAmount';
var amountEl = document.getElementById(amountElementId);

getCurrencySymbol().then((symbol) => {
    console.log('Setting up with currency symbol: ' + symbol);
    if (symbol === '$') {
        amountEl.classList.add('usd');
    } else if (symbol === '€') {
        amountEl.classList.add('eur');
    } else if (symbol === '£') {
        amountEl.classList.add('gbp');
    }
    drawTotal();
    setInterval(drawTotal, updateDelay);
});

function drawTotal(element) {
    fetchJSONFile(totalUrl, (data) => {
        // console.log(data);
        amountEl.innerText = data['total'];
    }, () => {
        markUnavailable();
    });
}

function markUnavailable() {
    var header = document.getElementById('overlay-amount');
    header.innerHTML = 'Connection error';
}
