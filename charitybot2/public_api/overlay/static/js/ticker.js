//var apiUrl = 'https://api.charitybot.net/api/v1/';
apiAddress = apiAddress + '/api/v1';
var eventUrl = apiAddress + '/event/' + eventIdentifier;
var donationsUrl = eventUrl + '/donations/';

var currencySymbol = 'N/A';

console.log('Connecting to API via: ' + apiAddress);

// Get the currency symbol then setup the updating cycle
getCurrencySymbol().then((symbol) => {
    currencySymbol = symbol;
    updateTicker(numberOfDonations);
    setInterval(
        () => {
            updateTicker(numberOfDonations);
        },
        updateDelay
    );
}).catch((error) => {
    console.error(error);
});

function updateTicker(limit) {
    fetchJSONFile(
        donationsUrl + '?limit=' + limit,
        (response) => {
            drawTableRows(response.donations);
        },
        () => {
            console.error('Unable to connect to retrieve donations');
        }
    );
}

function drawTableRows(donations) {
    var wrapperEl = document.getElementById('ticker-wrapper');
    // Clear out the old HTML first TODO: Remove this system
    wrapperEl.innerHTML = '';
    for (var i = 0; i < donations.length; i++) {
        var donation = JSON.parse(donations[i]);
        var rowEl = createRowEl(donation['amount'], donation['donor_name'], donation['timestamp']);

        rowEl.classList.add('row');
        wrapperEl.appendChild(rowEl);
    }
}

function createRowEl(amount, name, timestamp) {
    var parentEl = document.createElement('div');
    var textEl = document.createElement('p');
    textEl.classList.add('text');
    textEl.classList.add('fulljustify');
    name = name || 'Anonymous';
    var rowString = currencySymbol + amount + ' from ' + name + ', ' + returnTimespanString(((new Date()).getTime() / 1000) - timestamp) + ' ago';;
    textEl.innerText = rowString;
    parentEl.appendChild(textEl);
    return parentEl;
}