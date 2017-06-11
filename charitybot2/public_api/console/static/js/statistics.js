var apiUrl = 'http://127.0.0.1:8001/api/v1/';
var eventUrl = apiUrl + 'event/' + eventIdentifier;

drawUI();

function drawUI() {
    drawEventDetails();
}

function getConsoleElement(id) {
    return document.getElementById(id);
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