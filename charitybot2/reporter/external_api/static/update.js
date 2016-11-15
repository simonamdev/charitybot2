class OverlayUpdate {
    constructor(eventName) {
        this._eventName = eventName;
    }

    runUpdateCycle() {
        console.log('Updating');
        var lastDonationUrl = 'http://127.0.0.1:9000/event/' + this._eventName + '/donations/last';
        $.getJSON(lastDonationUrl, (data) => {
            console.log(data);
            $('#amount_raised').text(data['total_raised']);
        }).fail((data) => {
            console.log('Error');
            $('#amount_raised').text(data['error']);
        });
    }

    setupLoop() {
        setInterval(() => {
            this.runUpdateCycle();
        }, 2000);
    }
}
