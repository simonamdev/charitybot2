from .scraper import Scraper, SoupDataSources


class NoFundraiserNameGivenException(Exception):
    pass


class InvalidFundraiserUrlException(Exception):
    pass


class JustGivingScraper(Scraper):
    def __init__(self, fundraiser_name='', fundraiser_type='fundraising', verbose=False):
        self.fundraiser_name = fundraiser_name
        self.validate_fundraiser_name()
        self.verbose = verbose
        self.soup_data_sources = None
        self.base_url = 'https://www.justgiving.com/'
        self.fundraiser_url = self.base_url + fundraiser_type + '/' + fundraiser_name
        super().__init__(url=self.fundraiser_url, verbose=verbose)
        self.is_valid = False
        self.validate_scraper()
        self.setup_soup_data_sources()

    def print(self, print_string):
        if self.verbose:
            print('[JUSTGIVING] {0}'.format(print_string))

    def validate_fundraiser_name(self):
        if not self.fundraiser_name:
            raise NoFundraiserNameGivenException('Cannot start a JustGiving object without a fundraiser name')

    def validate_scraper(self):
        if not self.url_is_valid:
            raise InvalidFundraiserUrlException('Fundraiser URL could not be validated. Make sure the name is correct?')
        self.print('Just Giving Scraper successfully validated')
        self.is_valid = True

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
        self.get_soup_from_url()
        return self.url_soup.find(
            self.soup_data_sources.get_source_tag(source_name=source_name),
            self.soup_data_sources.get_bs4_find_parameters_dict(source_name=source_name)
        ).text
