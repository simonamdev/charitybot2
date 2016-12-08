function setCurrency(eventName) {
    var eventDetailsUrl = 'http://127.0.0.1:9000/event/' + eventName;
    $.getJSON(eventDetailsUrl, (data) => {
        console.log(data);
        $('#currency_symbol').text(data['currency_symbol']);
    }).fail((data) => {
        console.error('Unable to set currency');
    })
}

function setDonationAmount(eventName) {
    var lastDonationUrl = 'http://127.0.0.1:9000/event/' + eventName + '/donations/last';
    $.getJSON(lastDonationUrl, (data) => {
        console.log(data);
        $('#amount_raised').text(data['total_raised']);
    }).fail((data) => {
        console.error('Unable to set amount raised');
    })
}
