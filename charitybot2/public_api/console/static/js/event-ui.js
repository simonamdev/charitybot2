var apiUrl = 'http://127.0.0.1:8001/api/v1/';
var debugMode = true;
var currencyKey = "";

eventUI();

function eventUI() {
    getEventDetails(eventIdentifier);
    getDonations(eventIdentifier);
}

function debugPrint(log) {
    if (debugMode) {
        console.log(log);
    }
}

function getEventDetails(eventIdentifier) {
    console.log('Retrieving data for event: ' + eventIdentifier);
    var url = apiUrl + 'event/' + eventIdentifier;
    $.getJSON(url, data => {
        setupCurrencyKey(data);
        drawEventDetails(data);
    }).fail(() => {
        console.error('Could not reach URL: ' + url);
    });
}

function setupCurrencyKey(data) {
    currencyKey = data['currency_key'];
}

function drawEventDetails(data) {
    debugPrint(data);
    $('#event-header').text(data['title']);
}

function getDonations(eventIdentifier, lowerTimeBound, upperTimeBound) {
    console.log('Retrieving donation data for: ' + eventIdentifier + ' between ' + lowerTimeBound + ' and ' + upperTimeBound);
    var url = apiUrl + 'event/' + eventIdentifier + '/donations';
    $.getJSON(url, data => {
        drawDonations(data);
    }).fail(() => {
        console.error('Could not reach URL: ' + url);
    });
}

function drawDonations(data) {
    debugPrint(data);
    var donationsData = data['donations'];
    var donationsTable = $('#donations-table');
    for (i = 0; i < donationsData.length; i++) {
        var rowDonation = JSON.parse(donationsData[i]);
        var rowString = '<tr><td>' +
                        rowDonation['identifier'] +
                        '</td><td>' +
                        rowDonation['amount'] +
                        '</td><td>' +
                        rowDonation['timestamp'] +
                        '</td><td>' +
                        rowDonation['notes']
                        '</td></tr>'
        $('#donations-table').append(rowString);
    }
}