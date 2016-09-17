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
        self.url_is_valid = self.check_url_is_valid()

    def check_url_is_valid(self):
        try:
            self.get.make_request()
        except smokesignal.exceptions.ConnectionFailedException:
            raise SourceUnavailableException('Scraper could not connect to url: {0}'.format(self.url))
        return self.get.get_response_code() == 200

    def get_url_contents(self):
        self.get.make_request()
        return self.get.get_response_contents()

    def get_soup_from_url(self):
        return BeautifulSoup(self.get_url_contents(), self.parser)


class SoupDataSourceNotRegisteredException(Exception):
    pass


class InvalidSoupSourceNameGiven(Exception):
    pass


class SoupDataSources:
    """
    This class represents the locations on an HTML page where specific sources (such as amount raised
    or number of donations) can be found.
    """
    def __init__(self):
        self.sources = {}
        self.source_names = [
            'amount_raised',
            'amount_target',
            'last_donation_name',
            'last_donation_source',
            'last_donation_amount',
            'last_donation_message',
            'last_donation_timestamp',
            'last_donation_giftaid'
        ]

    # Reference: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    def set_source(self, source_name, tag_type, tag_class='', tag_id=''):
        if not self.is_source_valid(source_name=source_name):
            raise InvalidSoupSourceNameGiven('')
        # Remove the # from the id
        tag_id = tag_id.replace('#', '')
        self.sources[source_name] = {
            'tag': tag_type,
            'class': tag_class,
            'id': tag_id
        }

    def is_source_valid(self, source_name):
        return source_name in self.source_names

    # Get the dictionary for parameters, translated from the internal SoupDataSources dictionary to what BS4 understands
    def get_bs4_find_parameters_dict(self, source_name):
        return {
            'class': self.get_source_class(source_name=source_name),
            'id': self.get_source_id(source_name=source_name)
        }

    def get_source_tag(self, source_name):
        return self.get_source_attribute(source_name=source_name, attribute='tag')

    def get_source_class(self, source_name):
        return self.get_source_attribute(source_name=source_name, attribute='class')

    def get_source_id(self, source_name):
        return self.get_source_attribute(source_name=source_name, attribute='id')

    def get_source_attribute(self, source_name, attribute):
        if not self.source_available(source_name=source_name):
            raise SoupDataSourceNotRegisteredException
        return self.sources[source_name][attribute]

    def source_available(self, source_name):
        return source_name in self.sources

    def get_available_source_names(self):
        return tuple(self.sources.keys())
