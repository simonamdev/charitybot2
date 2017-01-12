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
        self.debug = debug
        self.logger = Logger(source='JustGivingScraper', event='', console_only=self.debug)
        self.soup_data_sources = None
        try:
            super().__init__(url=self.url, debug=debug)
        except SourceUnavailableException:
            raise InvalidFundraiserUrlException
        self.setup_soup_data_sources()

    def setup_soup_data_sources(self):
        sds = SoupDataSources()
        sds.set_source(
            source_name='amount_raised',
            tag_type='span',
            tag_class='statistics-amount-raised theme-highlight-text-font'
        )
        self.soup_data_sources = sds
        self.logger.log_info('Just Giving Scraper sources initialised with {0} sources'.format(
            len(sds.get_available_source_names())))

    def get_all_source_values(self):
        for source_name in self.soup_data_sources.get_available_source_names():
            self.logger.log_verbose('Retrieiving the value of: {0}'.format(source_name))
            value = self.get_source_value(source_name=source_name)
            print(value)

    def scrape_amount_raised(self):
        return self.get_source_value(source_name='amount_raised')

    def get_source_value(self, source_name):
        try:
            source_value = self.get_soup_from_url().find(
                self.soup_data_sources.get_source_tag(source_name=source_name),
                self.soup_data_sources.get_bs4_find_parameters_dict(source_name=source_name)
            ).text
        except ConnectionFailedException:
            raise SourceUnavailableException('Unable to connect to the source')
        except AttributeError:
            raise SourceUnavailableException('Unable to find amount raised on JustGiving website')
        return source_value

