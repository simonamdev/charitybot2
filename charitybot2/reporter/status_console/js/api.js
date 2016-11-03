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
        var api_url = this._url + 'event/' + eventName;
        $.getJSON(api_url, (data)=> {
            console.log(data);
            $('#event_name').text(data['name']);
            $('#donation_count').text(data['donation_count']);
            $('#donation_average').text(data['donation_average']);
            $('#largest_donation').text(data['largest_donation']);
        });
    }
};