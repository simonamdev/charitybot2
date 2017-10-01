//var apiUrl = 'https://api.charitybot.net/api/v1/';
apiAddress = apiAddress + '/api/v1';
var eventUrl = apiAddress + '/event/' + eventIdentifier;
var donationsUrl = eventUrl + '/donations/';

var currencySymbol = 'N/A';
var currentDonations = [];

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
            var parsedDonationData = parseDonations(response.donations);
            renderCurrentDonations(parsedDonationData);
        },
        () => {
            console.error('Unable to connect to retrieve donations');
        }
    );
}

function parseDonations(donationsFromApi) {
    // Get new donations to keep
    var donationsToKeep = donationsFromApi.filter((donation) => {
        if (currentDonations.indexOf(donation) !== -1) {
            return donation;
        }
    });
    // Get donations to add
    var donationsToAdd = donationsFromApi.filter((donation) => {
        if (currentDonations.indexOf(donation) === -1) {
            return donation;
        }
    });
    // Get donations to remove
    var donationsToRemove = currentDonations.filter((donation) => {
        if (donationsFromApi.indexOf(donation) === -1) {
            return donation;
        }
    });
//    console.log(donationsToKeep);
//    console.log(donationsToAdd);
//    console.log(donationsToRemove);
    currentDonations = donationsToKeep;
    currentDonations = currentDonations.concat(donationsToAdd);
    return {
        'keep': donationsToKeep,
        'add': donationsToAdd,
        'remove': donationsToRemove
    };
}

function renderCurrentDonations(parsedDonationData) {
    var donationsToAdd = parsedDonationData['add'];
    var donationsToRemove = parsedDonationData['remove'];
    var wrapperEl = document.getElementById('ticker-wrapper');
    // Hide donations to be removed
    for (var i = 0; i < donationsToRemove.length; i++) {
        let donation = JSON.parse(donationsToRemove[i]);
        // console.log(donation);
        let relevantTextEl = document.getElementById(donation['internal_reference']);
        // TODO: Instead of hiding, add a css class which animates it out, then remove it
        let rowToRemoveEl = relevantTextEl.parentNode;
        // console.log(rowToRemoveEl);
        setTimeout(() => {
            rowToRemoveEl.classList.add('zoomOut');
            setTimeout(() => {
                rowToRemoveEl.parentNode.removeChild(rowToRemoveEl);
            }, 100);
        }, 500);
    }
    // Add new donations
    for (var i = donationsToAdd.length - 1; i >= 0; i--) {
        let donation = JSON.parse(donationsToAdd[i]);
        // console.log(donation);
        let rowEl = createRowEl(
            donation['amount'],
            donation['donor_name'],
            donation['timestamp'],
            donation['internal_reference']
        );
        rowEl.classList.add('row');
        rowEl.classList.add('animated');
        rowEl.classList.add('zoomInUp');
        // Add the first set instantly
        if (donationsToRemove.length == 0) {
            wrapperEl.insertBefore(rowEl, wrapperEl.firstChild);
        } else {
            setTimeout(() => {
                wrapperEl.insertBefore(rowEl, wrapperEl.firstChild);
            }, 500);
        }
    }
}

function createRowEl(amount, name, timestamp, id) {
    var parentEl = document.createElement('div');
    var textEl = document.createElement('p');
    // Setting the ID lets us remove it from the list later
    textEl.id = id;
    textEl.classList.add('text');
    textEl.classList.add('fulljustify');
    name = name || 'Anonymous';
    var rowString = currencySymbol + amount + ' from ' + name;
    textEl.innerText = rowString;
    parentEl.appendChild(textEl);
    return parentEl;
}