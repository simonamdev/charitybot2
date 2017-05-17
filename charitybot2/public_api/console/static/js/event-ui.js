var apiUrl = 'http://127.0.0.1:8001/api/v1/';
var debugMode = true;
var currencyKey = "";
var currencySymbol = "";

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
        setupCurrency(data);
        drawEventDetails(data);
    }).fail(() => {
        console.error('Could not reach URL: ' + url);
    });
}

function setupCurrency(data) {
    currencyKey = data['currency_key'];
    // TODO: Move this to a function
    if (currencyKey == 'EUR') {
        currencySymbol = '€';
    } else if (currencyKey == 'USD') {
        currencySymbol = '$';
    } else {
        currencySymbol = '£';
    }
}

// TODO: Add switch for standard, european, american timestamp order
function convertTimestampToDatetime(timestamp) {
    if (timestamp >= 2147483647) {
    return 'Heat Death of the Universe';
  }
  var d = new Date(timestamp * 1000);
  var day = d.getDate();
  var month = d.getMonth() + 1;
  var hours = d.getHours();
  var minutes = d.getMinutes();
  var seconds = d.getSeconds();
  if (day < 10) {
     day = '0' + day;
  }
  if (month < 10) {
    month = '0' + month;
  }
  if (hours < 10) {
    hours = '0' + hours;
  }
  if (minutes < 10) {
    minutes = '0' + minutes;
  }
  if (seconds < 10) {
    seconds = '0' + seconds;
  }
  return d.getFullYear() + '/' + month + '/' + day + ' ' + hours + ':' + minutes + ':' + seconds;
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
                        i +
                        '</td><td>' +
                        currencySymbol + rowDonation['amount'] +
                        '</td><td>' +
                        convertTimestampToDatetime(rowDonation['timestamp']) +
                        '</td><td>' +
                        rowDonation['donor_name'] +
                        '</td><td>' +
                        rowDonation['external_reference']
                        '</td></tr>'
        $('#donations-table').append(rowString);
    }
}