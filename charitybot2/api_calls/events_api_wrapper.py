import json

from charitybot2.sources.url_call import UrlCall


class EventsApiWrapper:
    def __init__(self, base_url, version=2, timeout=2, maximum_retry_attempts=3):
        self._base_url = base_url + 'api/v{}/'.format(version)  # TODO: Use path resolving function instead of string concat
        self._timeout = timeout
        self._maximum_retry_attempts = maximum_retry_attempts

    def get_index(self):
        return json.loads(UrlCall(url=self._base_url, timeout=self._timeout).get().content.decode('utf-8'))
