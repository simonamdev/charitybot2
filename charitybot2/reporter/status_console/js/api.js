class API {
    constructor(url) {
        this._url = url;
    }

    setupEventInformation(eventName) {
        var api_url = this._url + 'events/' + eventName;
        $.getJSON(api_url, (data)=> {
            console.log(data);
        });
    }
};