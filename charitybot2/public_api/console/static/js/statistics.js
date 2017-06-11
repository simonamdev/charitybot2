var apiUrl = 'http://127.0.0.1:8001/api/v1/';
var eventUrl = apiUrl + 'event/' + eventIdentifier;
var eventExistenceUrl = apiUrl + 'event/exists/' + eventIdentifier;

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
            (apiData) => {
                var data = JSON.parse(apiData);
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
                resolve(data)
            },
            (error) => {
                reject(error);
            }
        );
    });
}

function drawEventDetails() {
    getEventDetails().then(
        (apiData) => {
            var data = JSON.parse(apiData);
            getConsoleElement('eventStartTime').innerHTML = data['start_time'];
            getConsoleElement('eventEndTime').innerHTML = data['end_time'];
        }
    ).catch((error) => {
        console.error(error);
    });
}

function getEventDetails() {
    return new Promise((resolve, reject) => {
        sendGetRequest(
            eventUrl,
            (data) => {
                resolve(data)
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