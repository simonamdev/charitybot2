from smokesignal.exceptions import ConnectionFailedException

from .scraper import Scraper, SoupDataSources, SourceUnavailableException


class NoFundraiserNameGivenException(Exception):
    pass


class InvalidFundraiserUrlException(Exception):
    pass


class JustGivingScraper(Scraper):
    def __init__(self, url, verbose=False):
        self.url = url
        self.verbose = verbose
        self.soup_data_sources = None
        try:
            super().__init__(url=self.url, verbose=verbose)
        except SourceUnavailableException:
            raise InvalidFundraiserUrlException
        self.setup_soup_data_sources()

    def print(self, print_string):
        if self.verbose:
            print('[JUSTGIVING] {0}'.format(print_string))

    def setup_soup_data_sources(self):
        sds = SoupDataSources()
        sds.set_source(
            source_name='amount_raised',
            tag_type='span',
            tag_class='statistics-amount-raised theme-highlight-text-font'
        )
        self.soup_data_sources = sds
        self.print('Just Giving Scraper sources initialised with {0} sources'.format(len(sds.get_available_source_names())))

    def get_all_source_values(self):
        for source_name in self.soup_data_sources.get_available_source_names():
            self.print('Retrieiving the value of: {0}'.format(source_name))
            value = self.get_source_value(source_name=source_name)
            print(value)

    def get_source_value(self, source_name):
        try:
            self.get_soup_from_url()
        except ConnectionFailedException:
            raise SourceUnavailableException('Unable to connect to the source')
        return self.url_soup.find(
            self.soup_data_sources.get_source_tag(source_name=source_name),
            self.soup_data_sources.get_bs4_find_parameters_dict(source_name=source_name)
        ).text

    def get_amount_raised(self):
        return self.get_source_value(source_name='amount_raised')
