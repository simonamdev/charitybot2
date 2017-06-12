var apiUrl = 'http://127.0.0.1:8001/api/v1/';
var eventUrl = apiUrl + 'event/' + eventIdentifier;
var eventExistenceUrl = apiUrl + 'event/exists/' + eventIdentifier;
var eventTotalUrl = eventUrl + '/total/';

drawUI();

function drawUI() {
    checkEventExists().then((eventExists) => {
        if (eventExists) {
            drawEventDetails();
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
    return new Promise((resolve, reject) => {
        sendGetRequest(
            eventExistenceUrl,
            (data) => {
                resolve(JSON.parse(data))
            },
            (error) => {
                reject(error);
            }
        );
    });
}

function drawEventDetails() {
    getEventData().then(
        (data) => {
            var eventDetails = data[0];
            var eventTotal = data[1]['total'];
            // Event Details
            getConsoleElement('eventStartTime').innerHTML = eventDetails['start_time'];
            getConsoleElement('eventEndTime').innerHTML = eventDetails['end_time'];
            // Event amounts
            getConsoleElement('eventAmountRaised').innerHTML = eventTotal;
            getConsoleElement('eventTargetRaised').innerHTML = eventDetails['target_amount'];
        }
    ).catch((error) => {
        console.error(error);
    });
}

function getEventData() {
    var eventDetailsPromise = new Promise((resolve, reject) => {
        sendGetRequest(
            eventUrl,
            (data) => {
                resolve(JSON.parse(data))
            },
            (error) => {
                reject(error);
            }
        );
    });
    var eventTotalPromise = new Promise((resolve, reject) => {
        sendGetRequest(
            eventTotalUrl,
            (data) => {
                resolve(JSON.parse(data))
            },
            (error) => {
                reject(error);
            }
        );
    });
    return Promise.all([eventDetailsPromise, eventTotalPromise]);
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