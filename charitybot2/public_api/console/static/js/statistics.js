var apiUrl = 'http://127.0.0.1:8001/api/v1/';
var eventUrl = apiUrl + 'event/' + eventIdentifier;
var eventExistenceUrl = apiUrl + 'event/exists/' + eventIdentifier;
var eventTotalUrl = eventUrl + '/total/';
var donationsUrl = eventUrl + '/donations/';
var donationCountUrl = donationsUrl + 'count';

drawUI();

function drawUI() {
    checkEventExists().then((eventExists) => {
        if (eventExists) {
            drawCurrencySymbolOnPage();
            drawEventDetails();
            drawDonationData();
        }
    });
}

function getConsoleElement(id) {
    return document.getElementById(id);
}

function checkEventExists() {
    getConsoleElement('event-alert').style.display = 'none';
    return new Promise((resolve, reject) => {
        getEventExistence().then(
            (data) => {
                if (!data['event_exists']) {
                    // Clear the screen and unhide the error
                    getConsoleElement('event-alert').style.display = 'block';
                    getConsoleElement('statisticsConsole').style.display = 'none';
                    resolve(false);
                }
                resolve(true);
            }
        ).catch((error) => {
            console.error(error);
            reject(false);
        });
    });
}

function getEventExistence() {
    return getDataFromApi(eventExistenceUrl);
}

function drawEventDetails() {
    getEventData().then(
        (data) => {
            var eventDetails = data[0];
            var eventTotal = data[1]['total'];
            // Event Details
            getConsoleElement('eventStartTime').innerHTML = convertToDatetime(eventDetails['start_time']);
            getConsoleElement('eventEndTime').innerHTML = convertToDatetime(eventDetails['end_time']);
            // Event amounts
            getConsoleElement('eventAmountRaised').innerHTML = eventTotal;
            getConsoleElement('eventTargetRaised').innerHTML = eventDetails['target_amount'];
            // Progress bar
            var currentTime = Math.floor(Date.now() / 1000);
            var completedEventPercentage = (parseInt(eventDetails['end_time']) - currentTime) /
                                      (parseInt(eventDetails['end_time']) - parseInt(eventDetails['start_time']));
            completedEventPercentage = Math.round(completedEventPercentage * 100);
            // TODO: Progress bar for event
            var donationCompletionPercentage = parseInt(eventTotal) / parseInt(eventDetails['target_amount']);
            donationCompletionPercentage = Math.round(donationCompletionPercentage * 100);
            // TODO: Progress bar for donations
        }
    ).catch((error) => {
        console.error(error);
    });
}

function getEventData() {
    var eventDetailsPromise = getDataFromApi(eventUrl);
    var eventTotalPromise = getDataFromApi(eventTotalUrl);
    return Promise.all([eventDetailsPromise, eventTotalPromise]);
}

function drawDonationData() {
    getDonationData().then(
        (data) => {
            var donationCount = data[0]['count'];
            var timeBoundCount = data[1]['count'];
            var largestDonation = data[2];
            var latestDonation = JSON.parse(data[3]['donations']);
            getConsoleElement('donationCount').innerHTML = donationCount;
            getConsoleElement('donationCountInTimespan').innerHTML = timeBoundCount + ' donations in the last 5 minutes';
            // TODO: Average donation drawing
            getConsoleElement('largestDonationAmount').innerHTML = largestDonation['amount'];
            getConsoleElement('latestDonationAmount').innerHTML = latestDonation['amount'];
            // TODO: Donation progress bar
        }
    ).catch((error) => {
        console.log(error);
    });
}

function getDonationData() {
    var donationCountPromise = getDataFromApi(donationCountUrl)
    // Donation count in last 5 minutes
    var now = new Date().getTime();
    var five_minutes_ago = (now / 1000) - (5 * 60);
    var timeBoundUrl = donationCountUrl + '?lower=' + Math.round(five_minutes_ago) + '&upper=' + Math.round(now);
    var timeBoundDonationCountPromise = getDataFromApi(timeBoundUrl);
    var largestDonationPromise = getDataFromApi(donationsUrl + 'largest');
    var latestDonationPromise = getDataFromApi(donationsUrl + '?limit=1');
    // TODO: Average donation promise
    return Promise.all(
        [
            donationCountPromise,
            timeBoundDonationCountPromise,
            largestDonationPromise,
            latestDonationPromise
        ]
    );
}

function getDataFromApi(url) {
    return new Promise((resolve, reject) => {
        sendGetRequest(
            url,
            (data) => {
                resolve(JSON.parse(data))
            },
            (error) => {
                reject(error);
            }
        );
    });
}

function sendGetRequest(url, successCallback, failureCallback) {
    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = () => {
    var DONE = 4; // readyState 4 means the request is done.
    var OK = 200; // status 200 is a successful return.
    if (xhr.readyState === DONE) {
        if (xhr.status === OK) {
            successCallback(xhr.responseText);
        } else {
            failureCallback('Error: ' + xhr.status);
        }
      }
    };

    xhr.open('GET', url);
    xhr.send(null);
}