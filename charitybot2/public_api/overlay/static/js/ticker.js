var numberOfDonations = 10;

var apiUrl = 'http://127.0.0.1:8001/api/v1/';
var eventUrl = apiUrl + 'event/' + eventIdentifier;
var donationsUrl = eventUrl + '/donations/';

updateTicker(numberOfDonations);

function updateTicker(limit) {
    fetchJSONFile(
        donationsUrl + '?limit=' + limit,
        (response) => {
            drawTableRows(response);
        },
        () => {
            console.error('Unable to connect to retrieve donations');
        });
}

function drawTableRows(data) {
    var table = document.getElementById('ticker-table');
    var tableHeader = '<tr><th>Timestamp</th><th>Amount</th></tr>';
    table.innerHTML = '';
    table.innerHTML = tableHeader;
    var tableRows = '';
    for (var i = 0; i < data.donations.length; i++) {
        var donation = JSON.parse(data.donations[i]);
        var tableRow = '<tr><td>' + donation['timestamp'] + '</td><td>' + donation['amount'] + '</td></tr>';
        tableRows += tableRow;
    }
    table.innerHTML += tableRows;
}