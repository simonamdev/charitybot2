import requests


class ConnectionFailedException(Exception):
    pass


class UrlCall:
    def __init__(self, url, params=None, timeout=2):
        self.url = url
        self.params = params if params is not None else {}
        self.timeout = timeout

    def make_request(self, request_function):
        try:
            return request_function()
        except requests.exceptions.ConnectionError:
            raise ConnectionFailedException('Failed to establish a connection to: {}'.format(self.url))
        except requests.exceptions.TooManyRedirects:
            raise ConnectionFailedException('Too many redirects when connecting to: {}'.format(self.url))
        except requests.exceptions.MissingSchema:
            raise ConnectionFailedException('No schema passed for the url: {}'.format(self.url))

    def get(self):
        return self.make_request(
            request_function=lambda: requests.get(url=self.url, params=self.params, timeout=self.timeout))
