function getDataFromApi(url, params) {
    return new Promise((resolve, reject) => {
        sendGetRequest(
            url,
            params,
            (data) => {
                resolve(JSON.parse(data))
            },
            (error) => {
                reject(error);
            }
        );
    });
}

function sendGetRequest(url, params, successCallback, failureCallback) {
    var xhr = new XMLHttpRequest();
    if (params) {
        url = url + '?' + encodeQueryData(params);
    }

    xhr.onreadystatechange = () => {
    var DONE = 4; // readyState 4 means the request is done.
    var OK = 200; // status 200 is a successful return.
    if (xhr.readyState === DONE) {
        if (xhr.status === OK) {
            successCallback(xhr.responseText);
        } else {
            failureCallback('Error: ' + xhr.status);
        }
      }
    };

    xhr.open('GET', url);
    xhr.send(null);
}

function encodeQueryData(data) {
    let ret = [];
    for (let d in data) {
        ret.push(encodeURIComponent(d) + '=' + encodeURIComponent(data[d]));
    }
    return ret.join('&');
 }

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