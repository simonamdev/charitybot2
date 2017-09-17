//var apiUrl = 'https://api.charitybot.net/api/v1/';
apiAddress = apiAddress + '/api/v1';
var eventUrl = apiAddress + '/event/' + eventIdentifier;
var eventExistenceUrl = apiAddress + '/event/exists/' + eventIdentifier;
var donationsUrl = eventUrl + '/donations/';

var currencySymbol = '';

checkEventExists().then((eventExists) => {
    // Start updating the UI every updateDelay
    if (eventExists) {
        setupCurrencyKey().then(() => {
            refreshTable();
            setInterval(() => {
                refreshTable();
            }, 5000);
        });
    }
});

function refreshTable() {
    getDataFromApi(donationsUrl).then((data) => {
        drawDonations(data);
    });
}

function drawDonations(data) {
    var donationsData = data['donations'];
    var donationsTableBody = document.getElementById('donationsTableBody');
    // Clear the old data
    donationsTableBody.innerHTML = '';
    // Add in the rows
    var donationCount = limit < donationsData.length ? limit : donationsData.length ;
    for (let i = 0; i < donationCount; i++) {
        var rowDonation = JSON.parse(donationsData[i]);
        let rowString = '<tr><td data-label="Index">' +
                        i +
                        '</td><td data-label="Amount">' +
                        currencySymbol + rowDonation['amount'] +
                        '</td><td data-label="Time Ago">' +
                        returnTimespanString(Math.round((new Date()).getTime() / 1000) - rowDonation['timestamp']) +
                        ' ago</td><td data-label="Timestamp">' +
                        convertToDatetime(rowDonation['timestamp']) +
                        '</td><td data-label="Donor Name">' +
                        rowDonation['donor_name'] +
                        '</td>' +
                        getNoteTd(rowDonation['notes']) +
                        '<td data-label="External Ref">' +
                        rowDonation['external_reference'] +
                        '</td><td data-label="Internal Ref">' +
                        rowDonation['internal_reference'].substring(0, 8) +
                        '...</td></tr>';
        donationsTableBody.innerHTML += rowString;
    }
    delete donationsData;
}

function getNoteTd(note) {
    if (note.toLowerCase().indexOf('hunter') !== -1 && note.toLowerCase().indexOf('games') !== -1) {
        return '<td class="marked-row" data-label="Message">' + note + '</td>';
    }
    return '<td data-label="Message">' + note + '</td>';
}

function setupCurrencyKey() {
    return getDataFromApi(eventUrl).then(
        (data) => {
            currencyKey = data['currency_key'];
            if (currencyKey == 'EUR') {
                currencySymbol = '€';
            } else if (currencyKey == 'USD') {
                currencySymbol = '$';
            } else {
                currencySymbol = '£';
            }
        }
    );
}

// Check the event exists asynchronously
function checkEventExists() {
    return new Promise((resolve, reject) => {
        getDataFromApi(eventExistenceUrl).then(
            (data) => {
                if (!data['event_exists']) {
                    // Clear the screen and display the alert div
                    document.getElementById('alertDiv').style.display = 'block';
                    document.getElementById('alertMessageText').innerText = 'Event: ' + eventIdentifier + ' does not exist';
                    document.getElementById('statisticsDashboard').style.display = 'none';
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
