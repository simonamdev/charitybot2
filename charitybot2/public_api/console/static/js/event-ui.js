//var apiUrl = 'https://api.charitybot.net/api/v1/';
apiAddress = apiAddress + '/api/v1';
var eventUrl = apiAddress + '/event/' + eventIdentifier;
var eventExistenceUrl = apiAddress + '/event/exists/' + eventIdentifier;
var eventTotalUrl = eventUrl + '/total/';
var donationsUrl = eventUrl + '/donations/';
var donationCountUrl = donationsUrl + 'count';
var currencyKey = "";
var currencySymbol = "";

console.log('Connecting to API via: ' + apiAddress);
eventUI();

function eventUI() {
    $('#event-alert').hide();
    $('#donation-alert').hide();
    drawPageIfEventExists(eventIdentifier);
}

function drawPageIfEventExists(eventIdentifier) {
    var url = eventExistenceUrl;
    $.getJSON(url, data => {
        if (data['event_exists']) {
            drawPage();
        } else {
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
}

function getEventDetails(eventIdentifier) {
    var url = eventUrl;
    $.getJSON(url, data => {
        setupCurrency(data);
        drawEventDetails(data);
    }).fail(() => {
        console.error('Could not reach URL: ' + url);
    });
}

function drawEventDetails(data) {
    $('#eventHeader').text(data['title']);
    $('.currency-symbol').text(currencySymbol);
}

var newDonationUrl = apiAddress + '/donation/';

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
    request.open('POST', newDonationUrl, true);
    request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');

    // On load, handle if successful or not
    request.onload = () => {
        var response = JSON.parse(request.responseText);
        // If the donation was successful, redraw the donations
        if (response['received']) {
            getDonations(eventIdentifier);
            // Also redraw the statistics
            getStatistics(eventIdentifier);
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
