//var apiUrl = 'https://api.charitybot.net/api/v1/';
apiAddress = apiAddress + '/api/v1';
var eventUrl = apiAddress + '/event/' + eventIdentifier;
var eventExistenceUrl = apiAddress + '/event/exists/' + eventIdentifier;
var eventTotalUrl = eventUrl + '/total/';
var donationsUrl = eventUrl + '/donations/';
var donationCountUrl = donationsUrl + 'count';
var donationAverageUrl = donationsUrl + 'average';
var donationDistributionUrl = donationsUrl + 'distribution';

console.log('Connecting to API via: ' + apiAddress);
updateDelay = updateDelay || 10000; // ms
chartUpdateDelay = updateDelay * 3;

checkEventExists().then((eventExists) => {
    // Start updating the UI every updateDelay
    if (eventExists) {
        drawCurrencySymbolOnPage();
        drawEventDetails();
        drawDonationData();
        drawCharts();
        setInterval(() => {
            console.log('Drawing Console');
            drawDonationData();
        }, updateDelay);
        setInterval(() => {
            console.log('Drawing Charts');
            drawCharts();
        }, chartUpdateDelay);
    }
});

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

// Given a number, draw the event progress percentage
function drawEventPercentage(amount) {
    const minimumDivWidth = 12;
    let eventProgressEl = document.getElementById('eventProgressCard');
    let eventPercentageEl = document.getElementById('eventProgressPercentage');
    if (amount > 100) {
        eventPercentageEl.innerText = 'Event complete!';
        eventProgressEl.style.width = '100%';
    } else {
        eventPercentageEl.innerText = amount + '% complete';
        let width = amount >= minimumDivWidth ? amount : minimumDivWidth;
        eventProgressEl.style.width = width + '%';
    }
}

// Given a number, draw the donation progress percentage
function drawDonationPercentage(amount) {
    const minimumDivWidth = 19;
    let donationProgressEl = document.getElementById('donationProgressCard');
    let donationPercentageEl = document.getElementById('donationProgressPercentage');
    if (amount > 100) {
        donationPercentageEl.innerText = 'Target reached! ' + amount + '%';
        donationProgressEl.style.width = '100%';
    } else {
        donationPercentageEl.innerText = amount + '% reached';
        let width = amount >= minimumDivWidth ? amount : minimumDivWidth;
        donationProgressEl.style.width = width + '%';
    }
}

function drawEventDetails() {
    getEventData().then(
        (data) => {
            var eventDetails = data[0];
            var eventTotal = data[1]['total'];
            // Event Details
            document.getElementById('eventStartTime').innerHTML = convertToDatetime(eventDetails['start_time']);
            document.getElementById('eventEndTime').innerHTML = convertToDatetime(eventDetails['end_time']);
            // Event amounts
            document.getElementById('eventAmountRaised').innerHTML = eventTotal;
            document.getElementById('eventTargetRaised').innerHTML = eventDetails['target_amount'];
            // Progress bar
            var currentTime = Math.floor(Date.now() / 1000);
            var completedEventPercentage = (parseInt(eventDetails['end_time']) - currentTime) /
                                      (parseInt(eventDetails['end_time']) - parseInt(eventDetails['start_time']));
            completedEventPercentage = Math.round(completedEventPercentage * 100);
            completedEventPercentage = 100 - completedEventPercentage;
            drawEventPercentage(completedEventPercentage);

            var donationCompletionPercentage = parseInt(eventTotal) / parseInt(eventDetails['target_amount']);
            donationCompletionPercentage = Math.round(donationCompletionPercentage * 100);
            drawDonationPercentage(donationCompletionPercentage);
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
            var averageDonation = Math.round(data[4]['average_donation_amount']);
            document.getElementById('donationCount').innerHTML = donationCount;
            document.getElementById('donationCountInTimespan').innerHTML = timeBoundCount + ' donations in the last 5 minutes';
            document.getElementById('averageDonation').innerHTML = averageDonation;
            document.getElementById('largestDonation').innerHTML = largestDonation['amount'];
            document.getElementById('latestDonation').innerHTML = latestDonation['amount'];
        }
    ).catch((error) => {
        console.log(error);
    });
}

function getDonationData() {
    var donationCountPromise = getDataFromApi(donationCountUrl);
    // Donation count in last 5 minutes
    var now = new Date().getTime();
    var five_minutes_ago = (now / 1000) - (5 * 60);
    var timeBoundUrl = donationCountUrl + '?lower=' + Math.round(five_minutes_ago) + '&upper=' + Math.round(now);
    var timeBoundDonationCountPromise = getDataFromApi(timeBoundUrl);
    var largestDonationPromise = getDataFromApi(donationsUrl + 'largest');
    var latestDonationPromise = getDataFromApi(donationsUrl + '?limit=1');
    var averageDonationPromise = getDataFromApi(donationAverageUrl);
    return Promise.all(
        [
            donationCountPromise,
            timeBoundDonationCountPromise,
            largestDonationPromise,
            latestDonationPromise,
            averageDonationPromise
        ]
    );
}

function drawCharts() {
    var donationsPromise = getDataFromApi(donationsUrl);
    var distributionPromise = getDataFromApi(donationDistributionUrl);
    Promise.all([donationsPromise, distributionPromise]).then((data) => {
        let donations = data[0];
        let distribution = data[1];
        drawDonationsChart(donations['donations']);
        drawDonationsTotalChart(donations['donations']);
        drawDistributionChart(distribution);
    });
}

function drawDonationsChart(donations) {
    // adapt the data
    // Reverse the donations
    donations.reverse();
    let donationPoints = donations.map((donation) => {
        let parsedDonation = JSON.parse(donation);
        return {
            amount: parsedDonation.amount,
            timestamp: parsedDonation.timestamp
        };
    });
    // console.log(donationPoints);
    let canvasEl = document.getElementById('donationsOverTimeGraph');
    canvasEl.classList = 'ct-chart ct-square chart-canvas';
    // extract the series and labels
    let labels = donationPoints.map((donation) => {
        return convertToDatetime(donation['timestamp']);
    });
    let series = donationPoints.map((donation) => {
        return donation['amount'];
    });
    var data = {
        labels: labels,
        series: [
            series
        ]
    };
    return new Chartist.Line('#donationsOverTimeGraph', data);
}

function drawDonationsTotalChart(donations) {
    // adapt the data
    let donationPoints = donations.map((donation) => {
        let parsedDonation = JSON.parse(donation);
        return {
            amount: parsedDonation.amount,
            timestamp: parsedDonation.timestamp
        };
    });
    // console.log(donationPoints);
    let canvasEl = document.getElementById('donationsTotalOverTime');
    canvasEl.classList = 'ct-chart ct-square chart-canvas';
    let total = 0.0;
    let dataPoints = donationPoints.map((donation) => {
        total += parseFloat(donation['amount']);
        return {
            x: new Date(donation['timestamp'] * 1000),
            y: total
        };
    });
    let data = {
        series: [
            {
                name: 'Donation Total over time',
                data: dataPoints
            }
        ]
    };
    let options = {
        axisX: {
            type: Chartist.FixedScaleAxis,
            divisor: 5,
            labelInterpolationFnc: (value) => {
                return moment(value).format('D MMM YYYY HH:mm:ss');
            }
        }
    };
    return new Chartist.Line('#donationsTotalOverTime', data, options);
}

function drawDistributionChart(distribution) {
    // console.log(distribution);
    const bounds = [[0, 10], [10, 20], [20, 50], [50, 75], [75, 100], [100, 10000]];
    let labels = [];
    // Generate the bound labels
    for (let i = 0; i < bounds.length; i++) {
        labels.push(bounds[i].join(' -> '));
    }
    // console.log(labels);
    let canvasEl = document.getElementById('donationDistributionGraph');
    canvasEl.classList = 'ct-chart ct-square chart-canvas';
    new Chartist.Bar('#donationDistributionGraph', {
        labels: labels,
        series: distribution.distribution
    }, {
        distributeSeries: true,
        scales: {
            xAxes: [{
                barThickness: 50
            }]
        }
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