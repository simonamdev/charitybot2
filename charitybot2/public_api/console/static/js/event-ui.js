apiUrl = 'http://127.0.0.1:8001/api/v1/';
debugMode = true;

eventUI();

function eventUI() {
    getEventDetails(eventIdentifier);
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
        drawEventDetails(data);
    }).fail(() => {
        console.error('Could not reach URL: ' + url);
    });
}

function drawEventDetails(data) {
    debugPrint(data);
    $('#event-header').text(data['title']);
}