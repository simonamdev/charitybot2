//var apiUrl = 'https://api.charitybot.net/api/v1/';
apiAddress = apiAddress + '/api/v1';
var eventUrl = apiAddress + '/event/' + eventIdentifier;
var eventExistenceUrl = apiAddress + '/event/exists/' + eventIdentifier;
var eventTotalUrl = eventUrl + '/total/';
var donationsUrl = eventUrl + '/donations/';
var donationCountUrl = donationsUrl + 'count';
var newDonationUrl = apiAddress + '/donation/';
var currencyKey = "";
var currencySymbol = "";

console.log('Connecting to API via: ' + apiAddress);
drawPageIfEventExists(eventIdentifier);

function drawPageIfEventExists(eventIdentifier) {
    getDataFromApi(eventExistenceUrl).then((data) => {
         if (!data['event_exists']) {
            showAlert('Event: ' + eventIdentifier + ' does not exist');
        }
    });
}

function showAlert(message) {
    document.getElementById('alertDiv').style.display = 'block';
    document.getElementById('alertDivText').innerText = message;
}

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
    var amount = document.getElementById('newDonationAmount').value;
    var donor = document.getElementById('newDonationDonor').value;
    var notes = document.getElementById('newDonationNotes').value;
    // Clear form to avoid double clicking
    document.getElementById('newDonationAmount').value = '';
    document.getElementById('newDonationDonor').value = '';
    document.getElementById('newDonationNotes').value = '';
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
        if (!response['received']) {
            showAlert(response['message']);
        }
    };

    // If network error, show message
    request.onerror = () => {
        console.error('Error');
    };

    request.send(serializePostObject(data));
}
