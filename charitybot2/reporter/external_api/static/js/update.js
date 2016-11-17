class OverlayUpdate {
    constructor(eventName) {
        this._eventName = eventName;
    }

    setCurrency() {
        var eventDetailsUrl = 'http://127.0.0.1:9000/event/' + this._eventName;
        $.getJSON(eventDetailsUrl, (data) => {
            $('#currency_symbol').text(data['currency_symbol']);
        }).fail((data) => {
            console.error('Unable to set currency');
        })
    }

    runUpdateCycle() {
        this.setCurrency();
        var lastDonationUrl = 'http://127.0.0.1:9000/event/' + this._eventName + '/donations/last';
        this.setPendingCSS();
        $.getJSON(lastDonationUrl, (data) => {
            this.setAvailableCSS();
            $('#amount_raised').text(data['total_raised']);
        }).fail((data) => {
            this.setUnavailableCSS();
        });
    }

    setCurrencyAmountCSS(cssClass) {
        $('#currency_symbol').attr('class', cssClass);
        $('#amount_raised').attr('class', cssClass);
    }

    setAvailableCSS() {
        this.setCurrencyAmountCSS('available');
    }

    setPendingCSS() {
        this.setCurrencyAmountCSS('pending');
    }

    setUnavailableCSS() {
        this.setCurrencyAmountCSS('unavailable');
    }

    setupLoop() {
        setInterval(() => {
            this.runUpdateCycle();
        }, 4000);
    }
}
