apiAddress = apiAddress + '/api/v1';
var eventUrl = apiAddress + '/event/' + eventIdentifier;
var donationsUrl = eventUrl + '/donations';
var latestDonationUrl = donationsUrl + '?limit=1';

console.log('Connecting to API via: ' + apiAddress);

let previousDonation = null;


function getLatestDonation() {
//    console.log('Getting Latest Donation');
    fetchJSONFile(latestDonationUrl, (data) => {
        let latestDonation = JSON.parse(data['donations']);
        if (!previousDonation) {
            previousDonation = latestDonation;
        }
//        console.log(latest_donation);
        let latestEl = document.getElementById('overlay-latest');
        let name = latestDonation['donor_name'] || 'Anonymous';
        latestEl.innerHTML =
            latestDonation['amount'] +
            ' from ' +
            name +
            ', ' +
            returnTimespanString(Math.round((new Date()).getTime() / 1000) - latestDonation['timestamp']) +
            ' ago';
        let latestWrapperEl = document.getElementsByClassName('latest-wrapper')[0];
        if (previousDonation['internal_reference'] !== latestDonation['internal_reference']) {
            latestWrapperEl.classList.add('bounce');
            previousDonation = latestDonation;
        }
        // Animate then remove the class
        setTimeout(() => {
            latestWrapperEl.classList.remove('bounce');
        }, 1500);
    }, () => {
        markUnavailable();
    });
}

function markUnavailable() {
    let latest = document.getElementById('latest-header');
    latest.innerHTML = 'Unable to connect';
}

drawCurrencySymbolOnPage();
getLatestDonation();
setInterval(getLatestDonation, updateDelay)
