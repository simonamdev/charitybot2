// Reference:
// https://stackoverflow.com/questions/14388452/how-do-i-load-a-json-object-from-a-file-with-ajax

function fetchJSONFile(path, callback, failureCallback) {
    var httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function() {
        if (httpRequest.readyState === 4) {
            if (httpRequest.status === 200) {
                var text = httpRequest.responseText;
                var data = JSON.parse(text);
                if (callback) {
                    callback(data);
                }
            } else {
                failureCallback();
            }
        }
    };
    httpRequest.open('GET', path);
    httpRequest.send();
}