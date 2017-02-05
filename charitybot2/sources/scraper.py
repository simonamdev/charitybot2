from bs4 import BeautifulSoup
from charitybot2.sources.url_call import UrlCall, ConnectionFailedException
from charitybot2.storage.logger import Logger


class ScraperException(Exception):
    pass


class SourceUnavailableException(Exception):
    pass


class InvalidFundraiserUrlException(Exception):
    pass


class Scraper:
    def __init__(self, url, debug=False):
        self.url = url
        self.debug = debug
        self.logger = Logger(source='Scraper', event='', console_only=self.debug)
        self.parser = 'lxml'
        self.url_call = UrlCall(url=self.url)

    def validate_url(self):
        try:
            response = self.url_call.get()
        except ConnectionFailedException:
            return False
        return response.status_code == 200

    def get_data_from_url(self):
        response = None
        try:
            response = self.url_call.get()
        except ConnectionFailedException:
            if response is not None:
                self.logger.log_error('Received response code: {}'.format(response.status_code))
                self.logger.log_error('Received response content: {}'.format(response.content))
            raise SourceUnavailableException('Scraper could not connect to url: {0}'.format(self.url))
        return response

    def get_contents_from_url(self):
        contents = self.get_data_from_url().content.decode('utf-8')
        if self.debug:
            print('---- DEBUG OUTPUT ----')
            print(contents)
            print('---- DEBUG OUTPUT ----')
        return contents

    def get_soup(self, url_contents):
        return BeautifulSoup(url_contents, self.parser)

    def get_soup_from_url(self):
        return self.get_soup(self.get_contents_from_url())


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
