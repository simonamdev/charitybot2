function sortNumber(a,b) {
    return a - b;
}

class API {
    constructor(url) {
        this._url = url;
        this._eventInfo = {};
    }

    testRun() {
        showLoader();
        var api_call = this.showEventInformation('test');
        $.when(api_call).then(() => {
            hideLoader();
        });

    }

    showEventInformation(eventName) {
        var eventUrl = this._url + 'event/' + eventName;
        var donationsUrl = eventUrl + '/donations'
        $.getJSON(eventUrl, (data) => {
            console.log(data);
            this.writeEventDataToPage(data);
            this.writeCurrencySymbols(data['currency_symbol']);
        }).fail(() => {
            console.log('foobar');
        });
        $.getJSON(donationsUrl, (data) => {
            console.log(data);
            this.drawDonationsCharts(data);
        });
    }

    writeCurrencySymbols(currencySymbol) {
        $('.currency_symbol').text(currencySymbol);
    }

    writeEventDataToPage(data) {
        $('#event_name').text(data['name']);
        $('#donation_count').text(data['donation_count']);
        $('#donation_average').text(data['donation_average']);
        $('#largest_donation').text(data['largest_donation']);
    }

    drawDonationsCharts(data) {
        this.drawAmountRaisedChart(data['donations']);
        this.drawAmountHistogram(data['donations']);
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
                maintainAspectRatio: false,
                responsive: true
            }
        });
    }

    drawAmountHistogram(data) {
        var roundedAmounts = [];
        $.each(data, (index, object) => {
            roundedAmounts.push(Math.ceil(object['amount']));
        });
        roundedAmounts.sort(sortNumber);
        var counts = {};
        $.each(roundedAmounts, (index, amount) => {
            if (amount in counts) {
                counts[amount] += 1
            } else {
                counts[amount] = 1;
            }
        });
        var ctx =  $("#amountDistributionChart");
        var myBarChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: Object.keys(counts),
                datasets: [
                    {
                        label: 'Donation Amount Distribution',
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255,99,132,1)',
                        borderWidth: 1,
                        data: Object.values(counts)
                    }
                ]
            },
            options: {
                maintainAspectRatio: false,
                responsive: true,
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true,
                            stepSize: 1
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