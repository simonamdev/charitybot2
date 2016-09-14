from smokesignal import smokesignal
from bs4 import BeautifulSoup


class ScraperException(Exception):
    pass


class SourceUnavailableException(Exception):
    pass


class Scraper:
    def __init__(self, url, verbose=False):
        self.url = url
        self.parser = 'lxml'
        self.get = smokesignal.GetRequest(url=url, verbose=verbose)

    def is_url_valid(self):
        self.get.make_request()
        return self.get.get_response_code() == 200

    def get_url_contents(self):
        try:
            self.get.make_request()
        except smokesignal.exceptions.ConnectionFailedException:
            raise SourceUnavailableException('Could not connect to url: {0}'.format(self.url))
        return self.get.get_response_contents()

    def soup_url_contents(self):
        return BeautifulSoup(self.get_url_contents(), self.parser)
