from scraper.scraper import Scraper


class NoFundraiserNameGivenException(Exception):
    pass


class InvalidFundraiserUrlException(Exception):
    pass


class JustGivingScraper(Scraper):
    def __init__(self, fundraiser_name='', verbose=False):
        self.fundraiser_name = fundraiser_name
        self.base_url = 'https://www.justgiving.com/'
        self.fundraiser_url = self.base_url + 'fundraising/' + fundraiser_name
        super().__init__(url=self.fundraiser_url, verbose=verbose)
        self.is_valid = False
        self.validate_object()

    def validate_object(self):
        if not self.fundraiser_name:
            raise NoFundraiserNameGivenException('Cannot start a JustGiving object without a fundraiser name')
        if not self.is_url_valid():
            raise InvalidFundraiserUrlException('Fundraiser URL could not be validated. Make sure the name is correct?')
        self.is_valid = True
