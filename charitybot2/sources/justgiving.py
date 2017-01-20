from charitybot2.sources.url_call import ConnectionFailedException
from charitybot2.storage.logger import Logger

from .scraper import Scraper, SoupDataSources, SourceUnavailableException


class NoFundraiserNameGivenException(Exception):
    pass


class InvalidFundraiserUrlException(Exception):
    pass


class JustGivingScraper(Scraper):
    def __init__(self, url, debug=False):
        self.url = url
        self.type = self.__determine_type()
        self.debug = debug
        self.logger = Logger(source='JustGivingScraper', event='', console_only=self.debug)
        self.soup_data_sources = None
        try:
            super().__init__(url=self.url, debug=debug)
        except SourceUnavailableException:
            raise InvalidFundraiserUrlException
        self.setup_soup_data_sources()

    def __determine_type(self):
        if 'fundraising' in self.url:
            return 'fundraiser'
        elif 'campaign' in self.url:
            return 'campaign'
        else:
            raise InvalidFundraiserUrlException('Unable to discern fundraiser type from the Just Giving URL')

    def get_type(self):
        return self.type

    def setup_soup_data_sources(self):
        sds = SoupDataSources()
        sds.set_source(
            source_name='amount_raised',
            tag_type='span',
            tag_class='statistics-amount-raised theme-highlight-text-font'
        )
        self.soup_data_sources = sds
        self.logger.log_info('JustGiving Scraper sources initialised with {0} sources'.format(
            len(sds.get_available_source_names())))
        self.logger.log_info('JustGiving URL: {}'.format(self.url))

    def get_all_source_values(self):
        for source_name in self.soup_data_sources.get_available_source_names():
            self.logger.log_verbose('Retrieiving the value of: {0}'.format(source_name))
            value = self.get_source_value(source_name=source_name)
            print(value)

    def scrape_amount_raised(self):
        return self.get_source_value(source_name='amount_raised')

    def __get_source_value_from_url_contents(self, url_contents, source_name):
        try:
            source_value = self.get_soup(url_contents=url_contents).find(
                self.soup_data_sources.get_source_tag(source_name=source_name),
                self.soup_data_sources.get_bs4_find_parameters_dict(source_name=source_name)
            ).text
        except AttributeError:
            self.logger.log_error('Unable to find amount raised on Justgiving source')
            raise SourceUnavailableException('Unable to find amount raised on JustGiving website')
        return source_value

    def get_source_value(self, source_name):
        try:
            url_contents = self.get_contents_from_url()
            source_value = self.__get_source_value_from_url_contents(url_contents=url_contents, source_name=source_name)
        except ConnectionFailedException:
            self.logger.log_error('Unable to connect to the scraper source')
            raise SourceUnavailableException('Unable to connect to the source')
        return source_value

