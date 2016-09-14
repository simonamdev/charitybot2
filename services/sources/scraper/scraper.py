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
            raise SourceUnavailableException('Scraper could not connect to url: {0}'.format(self.url))
        return self.get.get_response_contents()

    def soup_url_contents(self):
        return BeautifulSoup(self.get_url_contents(), self.parser)


class SoupDataSourceNotRegisteredException(Exception):
    pass


class SoupDataSources:
    """
    This class represents the locations on an HTML page where specific sources (such as amount raised
    or number of donations) can be found.
    """
    def __init__(self):
        self.sources = {}

    def set_source(self, source_name, tag_type, tag_class='', tag_id=''):
        # TODO: Validate against a known set of tag types
        # TODO: Check if BS4 requires the # for a tag id and if not, remove it from the string
        self.sources[source_name] = {
            'tag': tag_type,
            'class': tag_class,
            'id': tag_id
        }

    # Get the dictionary for parameters, translated from the internal SoupDataSources dictionary to what BS4 understands
    def get_bs4_find_parameters(self, source_name):
        if not self.source_available(source_name=source_name):
            raise SoupDataSourceNotRegisteredException

    def source_available(self, source_name):
        return source_name in self.sources
