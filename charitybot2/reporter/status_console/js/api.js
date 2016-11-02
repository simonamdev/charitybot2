class API {
    constructor(url) {
        this._url = url;
    }

    setupEventInformation(eventName) {
        var api_url = this._url + 'event/' + eventName;
//        var api_url = '/event/' + eventName;
        $.getJSON(api_url, (data)=> {
            console.log(data);
        });
//        $.ajax({
//            url: "/event/" + eventName,
//            success: function(data) {
//                jsonData = JSON.parse(data);
//                console.log("Data received from API:");
//                console.log(jsonData);
//            }
//		});
    }
};