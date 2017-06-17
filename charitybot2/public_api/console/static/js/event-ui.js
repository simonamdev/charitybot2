var apiUrl = 'http://127.0.0.1:8001/api/v1/';
var debugMode = true;
var currencyKey = "";
var currencySymbol = "";

eventUI();

function eventUI() {
    $('#event-alert').hide();
    $('#donation-alert').hide();
    drawPageIfEventExists(eventIdentifier);
}

function debugPrint(log) {
    if (debugMode) {
        console.log(log);
    }
}

function drawPageIfEventExists(eventIdentifier) {
    var url = apiUrl + 'event/exists/' + eventIdentifier;
    $.getJSON(url, data => {
        if (data['event_exists']) {
            drawPage();
        } else {
            debugPrint('Event with identifier: ' + eventIdentifier + ' does not exist');
            $('#event-alert').show();
            $('#donations-table').hide();
            $('#statistics-div').hide();
        }
    }).fail(() => {
        console.error('Could not reach URL: ' + url);
        console.error('Could not confirm that event with identifier: ' + eventIdentifier + ' exists');
    });
}

function drawPage() {
    getEventDetails(eventIdentifier);
    getDonations(eventIdentifier);
    getStatistics(eventIdentifier);
}

function getEventDetails(eventIdentifier) {
    debugPrint('Retrieving data for event: ' + eventIdentifier);
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
    $('.currency-symbol').text(currencySymbol);
}

function getDonations(eventIdentifier, lowerTimeBound, upperTimeBound) {
    debugPrint('Retrieving donation data for: ' + eventIdentifier + ' between ' + lowerTimeBound + ' and ' + upperTimeBound);
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
    var donationsTableBody = $('#donations-table tbody');
    // Clear the old data
    donationsTableBody.empty();
    // Add in the rows
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
                        rowDonation['notes'] +
                        '</td><td>' +
                        rowDonation['external_reference'] +
                        '</td><td>' +
                        rowDonation['internal_reference'].substring(0, 8) +
                        '...' +
                        '</td></tr>'
        donationsTableBody.append(rowString);
    }
}

function getStatistics(eventIdentifier) {
    calls = [getEventTotal(eventIdentifier), getLastDonation(eventIdentifier)];
    $.when.apply($, calls).done((total, lastDonation) => {
        if (lastDonation[0]['donations'].length == 0) {
            drawStatistics(0);
        } else {
            drawStatistics(total[0]['total'], JSON.parse(lastDonation[0]['donations'])['timestamp']);
        }
    });
}

function getEventTotal(eventIdentifier) {
    var url = apiUrl + 'event/' + eventIdentifier + '/total/';
    return $.getJSON(url);
}

function getLastDonation(eventIdentifier) {
    var url = apiUrl + 'event/' + eventIdentifier + '/donations/?limit=1';
    return $.getJSON(url);
}

function drawStatistics(total, lastDonationTimestamp) {
    // Set the total
    debugPrint('Total Raised: ' + total);
    $('#donation-total').text(total);

    // Set the timespan if it is available
    if (lastDonationTimestamp) {
        debugPrint('Last Donation Timestamp: ' + lastDonationTimestamp);
        var currentTime = Math.round((new Date()).getTime() / 1000);
        var timeDifference = currentTime - lastDonationTimestamp;
        debugPrint(timeDifference);
        units = 'seconds';
        if (timeDifference > 60) {
            timeDifference /= 60;
            units = 'minutes';
            if (timeDifference > 60) {
                timeDifference /= 60;
                units = 'hours';
                if (timeDifference > 24) {
                    timeDifference /= 24;
                    units = 'days';
                }
            }
        }
        $('#donation-time-ago').text(timeDifference.toFixed(2) + ' ' + units + '  ago');
    } else {
        $('#donation-time-ago').text('N/A');
    }
}

var newDonationUrl = apiUrl + 'donation/';

function serializePostObject(obj) {
    var str = [];
    for(var p in obj)
    if (obj.hasOwnProperty(p)) {
        str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
    }
    return str.join("&");
}

function submitDonation() {
    // Get the values from the form
    var amount = $('#new-donation-amount').val();
    var donor = $('#new-donation-donor').val();
    var notes = $('#new-donation-notes').val();
    // Clear form to avoid double clicking
    $('#new-donation-amount').val('');
    $('#new-donation-donor').val('');
    $('#new-donation-notes').val('');
    // Validate the inputs

    // TODO

    // POST them to the API
    var request = new XMLHttpRequest();
    var data = {
        amount: amount,
        event_identifier: eventIdentifier,
        timestamp: Math.floor(Date.now() / 1000),
        donor_name: donor,
        notes: notes
    }
    debugPrint('Submitting following donation: ' + data);
    request.open('POST', newDonationUrl, true);
    request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');

    // On load, handle if successful or not
    request.onload = () => {
        var response = JSON.parse(request.responseText);
        debugPrint(response);
        // If the donation was successful, redraw the donations
        if (response['received']) {
            getDonations(eventIdentifier);
        } else {
            // Show an error with the message
            $('#donation-alert').show();
            $('#donation-alert p').text(response['message']);
        }
    };

    // If network error, show message
    request.onerror = () => {
        console.error('Error');
    };

    request.send(serializePostObject(data));
}
