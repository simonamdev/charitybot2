var apiUrl = 'http://127.0.0.1:8001/api/v1/';
var eventUrl = apiUrl + 'event/' + eventIdentifier;
var donationsUrl = eventUrl + '/donations';
var latestDonationUrl = donationsUrl + '?limit=1';

function getLatestDonation() {
    console.log('Getting Latest Donation');
    fetchJSONFile(latestDonationUrl, (data) => {
//        console.log(data);
        latest_donation = JSON.parse(data['donations']);
        var latest = document.getElementById('overlay-latest');
        latest.innerHTML =
            latest_donation['amount'] +
            ' from ' +
            latest_donation['donor_name'] +
            ', ' +
            returnTimespanString(latest_donation['timestamp']) +
            ' ago';
    }, () => {
        markUnavailable();
    });
}

function markUnavailable() {
    var latest = document.getElementById('latest-header');
    latest.innerHTML = 'Unable to connect';
}

drawCurrencySymbolOnPage();
getLatestDonation();
var updateDelay = 2000; // ms
setInterval(getLatestDonation, updateDelay)