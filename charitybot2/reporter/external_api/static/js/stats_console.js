function sortNumber(a,b) {
    return a - b;
}

// TODO: Move this to another file, for the sake of SRP
function resizeCanvasToWindowWidth(canvasID) {
    var canvas = $(canvasID);
    canvas.width($(window).width());
}

// Reference:
// https://stackoverflow.com/questions/2901102/how-to-print-a-number-with-commas-as-thousands-separators-in-javascript
function numberWithCommas(x) {
    if (x < 1000) {
        return x.toString();
    }
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function convertToTimestamp(unixTimestamp){
  if (unixTimestamp >= 2147483647) {
    return 'Heat Death of the Universe';
  }
  var d = new Date(unixTimestamp * 1000);
  var day = d.getDate();
  var month = d.getMonth() + 1;
  var hours = d.getHours();
  var minutes = d.getMinutes();
  var seconds = d.getSeconds();
  if (day < 10) {
     day = '0' + day;
  }
  if (month < 10) {
    month = '0' + month;
  }
  if (hours < 10) {
    hours = '0' + hours;
  }
  if (minutes < 10) {
    minutes = '0' + minutes;
  }
  if (seconds < 10) {
    seconds = '0' + seconds;
  }
  return day + '/' + month + '/' + d.getFullYear() + ' ' + hours + ':' + minutes + ':' + seconds;
}

function returnTimespanString(timespanInSeconds) {
    var timespanInMinutes = timespanInSeconds / 60;
    if (timespanInMinutes < 1) {
        return timespanInSeconds + ' seconds';
    } else if (timespanInMinutes == 1) {
        return 'second';
    }
    var timespanInHours = timespanInMinutes / 60;
    if (timespanInHours < 1) {
        return timespanInMinutes + ' minutes';
    } else if (timespanInMinutes == 1) {
        return 'minute';
    }
    if (timespanInHours == 1) {
        return 'hour';
    }
    return timespanInHours + ' hours';
}

class API {
    constructor(url, eventName) {
        this._url = url;
        this._eventName = eventName;
    }

    makeApiCalls() {
        showLoader();
        var api_call = this.writeAllDataToPage(this._eventName);
        $.when(api_call).then(() => {
            hideLoader();
        });
    }

    writeAllDataToPage() {
        // Event details
        var eventUrl = this._url + 'event/' + this._eventName;
        $.getJSON(eventUrl, (data) => {
            this.writeEventDetailsToPage(data);
            this.writeCurrencySymbols(data['currency_symbol']);
        }).fail(() => {
            console.log('Could not get event data');
        });
        // Donation details
        var donationsInfoUrl = eventUrl + '/donations/info';
        $.getJSON(donationsInfoUrl, (data) => {
            this.writeDonationDetailsToPage(data['donations_info']);
        }).fail(() => {
            console.log('Could not get donations info data');
        });
        // Donation Charts
        var donationsUrl = eventUrl + '/donations';
        $.getJSON(donationsUrl, (data) => {
            this.drawAmountRaisedChart(data['donations']);
        }).fail(() => {
            console.log('Could not get donations data');
        });
        var donationsDistributionUrl = donationsUrl + '/distribution';
        $.getJSON(donationsDistributionUrl, (data) => {
            this.drawDonationsDistributionChart(data['donations_distribution']);
        }).fail(() => {
            console.log('Could not get donation distribution data');
        });
    }

    writeCurrencySymbols(currencySymbol) {
        $('.currency-symbol').text(currencySymbol);
    }

    writeEventDetailsToPage(data) {
        console.log(data);
        // Event Length Data
        var startTime = data['start_time'];
        $('#event-start').text(convertToTimestamp(startTime));
        $('#event-end').text(convertToTimestamp(data['end_time']));
        var eventLength = Math.round(((data['end_time'] - startTime) / (60 * 60)) * 100) / 100;
        var currentTime = Math.floor(Date.now() / 1000);
        var eventTimeRemaining = Math.round((data['end_time'] - currentTime) * 100) / 100;
        var eventPercentageComplete = ((data['end_time'] - currentTime) / (data['end_time'] - startTime)) * 100;
        eventPercentageComplete = Math.abs(Math.round(eventPercentageComplete * 100) / 100);
        if (currentTime < startTime) {
            eventPercentageComplete = 100;
            eventTimeRemaining = startTime - currentTime;
            $('#event-time-remaining-column').text(numberWithCommas(Math.round(eventTimeRemaining / (60 * 60))) + ' hours till event start');
            $('#event-progress').text('Start Pending');
            $('#event-progress').toggleClass('progress-bar-danger');
        } else {
            if (eventPercentageComplete >= 100) {
                $('#event-progress').toggleClass('progress-bar-success');
            }
            $('#event-remaining').text(numberWithCommas(eventTimeRemaining));
            $('#event-progress').text(eventPercentageComplete + '%');
        }
        $('#event-progress').css('width', eventPercentageComplete + '%').attr('aria-valuenow', eventPercentageComplete);
        $('#event-length').text(numberWithCommas(eventLength));
        // Amount Raised Data
        $('#amount-raised').text(numberWithCommas(data['amount_raised']));
        $('#target-amount').text(numberWithCommas(data['target_amount']));
        var amountPercentageComplete = (data['amount_raised'] / data['target_amount']) * 100;
        amountPercentageComplete = Math.round(amountPercentageComplete * 100) / 100;
        $('#amount-progress').css('width', amountPercentageComplete + '%').attr('aria-valuenow', amountPercentageComplete).text(amountPercentageComplete + '%');
        if (amountPercentageComplete >= 100) {
            $('#amount-progress').toggleClass('progress-bar-success');
        }
    }

    writeDonationDetailsToPage(data) {
        console.log(data);
        $('#total-donation-count').text(data['count']);
        $('#donation-count').text(data['specific']['count']);
        $('#donation-timespan').text(returnTimespanString(data['specific']['timespan']));
        $('#average-donation').text(data['average']);
        var largest_donation = data['largest'];
        if (largest_donation != null) {
            $('#largest-donation').text(largest_donation['amount']);
            $('#largest-donation-timestamp').text(convertToTimestamp(largest_donation['timestamp']));
        } else {
            $('#largest-donation-column').text('Largest Donation: Waiting for a donation');
        }
        var last_donation = data['last'];
        if (last_donation != null) {
            $('#last-donation').text(last_donation['amount']);
            $('#last-donation-timestamp').text(convertToTimestamp(last_donation['timestamp']));
        } else {
            $('#last-donation-column').text('Last Donation: Waiting for a donation');
        }
    }

    drawAmountRaisedChart(data) {
        var labels = [];
        $.each(data, (index, object) => {
            var time = new Date(object['timestamp'] * 1000).toISOString().substring(11, 19);
            labels.push(time);
        });
        var values = [];
        $.each(data, (index, object) => {
            values.push(object['total_raised']);
        });
        var ctx =  $("#amountRaisedChart");
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Total Amount Raised',
                        lineTension: 0.05,
                        fill: true,
                        data: values,
                        borderColor: 'rgba(75,192,192,1)',
                        backgroundColor: 'rgba(75,192,192,0.3)'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: false
                        }
                    }]
                }
            }
        });
    }

    drawDonationsDistributionChart(data) {
        var sortedDistributions = [];
        // take out the unsortable key
        var largestCount = data['100-10000'];
        delete data['100-10000'];
        // place data in separate arrays
        var keys = [];
        var values = [];
        $.each(data, (key, count) => {
            keys.push(key);
            values.push(count);
        });
        // replace the unsortable key
        keys.push('100+');
        values.push(largestCount);
        var ctx =  $("#amountDistributionChart");
        var myBarChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: keys,
                datasets: [
                    {
                        label: 'Donation Amount Distribution',
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255,99,132,1)',
                        borderWidth: 1,
                        data: values
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }],
                    xAxes: [{
                        ticks: {
                            type: 'linear',
                            fixedStepSize: 1
                        }
                    }]
                }
            }
        });
    }
};