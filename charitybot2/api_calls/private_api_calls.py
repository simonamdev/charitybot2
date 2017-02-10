from charitybot2.private_api.private_api import private_api_full_url
from charitybot2.sources.url_call import UrlCall


class PrivateApiCalls:
    def __init__(self, timeout=2):
        self._timeout = timeout

    def get_index(self):
        return UrlCall(url=private_api_full_url, timeout=self._timeout).get()
