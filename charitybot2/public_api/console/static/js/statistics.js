drawUI();

function drawUI() {
    drawEventTitle();
}

function getConsoleElement(id) {
    return document.getElementById(id);
}

function drawEventTitle() {
    getConsoleElement('eventTitle').innerHTML = eventIdentifier;
}