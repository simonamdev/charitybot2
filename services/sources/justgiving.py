from scraper.scraper import Scraper, SoupDataSources


class NoFundraiserNameGivenException(Exception):
    pass


class InvalidFundraiserUrlException(Exception):
    pass


class JustGivingScraper(Scraper):
    def __init__(self, fundraiser_name='', verbose=False):
        self.fundraiser_name = fundraiser_name
        self.soup_data_sources = None
        self.base_url = 'https://www.justgiving.com/'
        self.fundraiser_url = self.base_url + 'fundraising/' + fundraiser_name
        super().__init__(url=self.fundraiser_url, verbose=verbose)
        self.is_valid = False
        self.validate_scraper()
        self.setup_soup_data_sources()

    def validate_scraper(self):
        if not self.fundraiser_name:
            raise NoFundraiserNameGivenException('Cannot start a JustGiving object without a fundraiser name')
        if not self.url_is_valid():
            raise InvalidFundraiserUrlException('Fundraiser URL could not be validated. Make sure the name is correct?')
        self.is_valid = True

    def setup_soup_data_sources(self):
        sds = SoupDataSources()
        sds.set_source(
            source_name='amount_raised',
            tag_type='span',
            tag_class='statistics-amount-raised theme-highlight-text-font'
        )
        self.soup_data_sources = sds
