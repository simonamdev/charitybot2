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
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function convertToTimestamp(unixTimestamp){
  var d = new Date(unixTimestamp * 1000);
  return d.getDate() + '/' + (d.getMonth() + 1) + '/' + d.getFullYear() + ' ' + d.getHours() + ':' + d.getMinutes() + ':' + d.getSeconds();
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
        var eventUrl = this._url + 'event/' + this._eventName;
        $.getJSON(eventUrl, (data) => {
            // console.log(data);
            this.writeEventDetailsToPage(data);
            this.writeCurrencySymbols(data['currency_symbol']);
        }).fail(() => {
            console.log('Could not get event data');
        });
        var donationsUrl = eventUrl + '/donations';
        $.getJSON(donationsUrl, (data) => {
            // console.log(data);
            this.writeAmountRaised(data['donations']);
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
        var lastDonationUrl = donationsUrl + '/last';
        $.getJSON(lastDonationUrl, (data) => {
            this.writeLastDonationAmount(data);
        }).fail(() => {
            console.log('Could not get last donation data');
        })
    }

    writeCurrencySymbols(currencySymbol) {
        $('.currency-symbol').text(currencySymbol);
    }

    writeEventDetailsToPage(data) {
        console.log(data);
        // Event Length Data
        $('#event-start').text(convertToTimestamp(data['start_time']));
        $('#event-end').text(convertToTimestamp(data['end_time']));
        var eventLength = Math.round(((data['end_time'] - data['start_time']) / (60 * 60)) * 100) / 100;
        var currentTime = Math.floor(Date.now() / 1000);
        var eventRemaining = Math.round((data['end_time'] - currentTime) * 100) / 100;
        var eventPercentageComplete = ((data['end_time'] - currentTime) / (data['end_time'] - data['start_time'])) * 100;
        eventPercentageComplete = Math.abs(Math.round(eventPercentageComplete * 100) / 100);
        $('#event-length').text(numberWithCommas(eventLength));
        $('#event-remaining').text(numberWithCommas(eventRemaining));
        $('#event-progress').css('width', eventPercentageComplete + '%').attr('aria-valuenow', eventPercentageComplete).text(eventPercentageComplete + '%');
        if (eventPercentageComplete >= 100) {
            $('#event-progress').toggleClass('progress-bar-success');
        }
        // Amount Raised Data
        $('#amount-raised').text(numberWithCommas(data['amount_raised']));
        $('#target-amount').text(numberWithCommas(data['target_amount']));
        var amountPercentageComplete = (data['amount_raised'] / data['target_amount']) * 100;
        amountPercentageComplete = Math.round(amountPercentageComplete * 100) / 100;
        console.log(amountPercentageComplete);
        $('#amount-progress').css('width', amountPercentageComplete + '%').attr('aria-valuenow', amountPercentageComplete).text(amountPercentageComplete + '%');
        if (amountPercentageComplete >= 100) {
            $('#amount-progress').toggleClass('progress-bar-success');
        }
        // Event Donation Data
        $('#donation_count').text(data['donation_count']);
        $('#donation_average').text(data['donation_average']);
        $('#largest_donation').text(data['largest_donation']);
        $('#last_hour_donation_count').text(data['last_hour_donation_count']);
    }

    writeLastDonationAmount(data) {
        $('#last_donation').text(data['amount']);
    }

    writeAmountRaised(data) {
        var prettyNumber = numberWithCommas(data[data.length - 1]['total_raised']);
        $('#amount_raised').text(prettyNumber);
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