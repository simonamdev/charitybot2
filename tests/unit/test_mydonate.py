import pytest
from charitybot2.sources.scraper import InvalidFundraiserUrlException


class TestMydonateScraperCreation:
    @pytest.mark.parametrize('url,except_expected', {
        '',
        'http://www.mydonate.com/blablalbal'
    })
    def test_creating_with_invalid_url_throws_exception(self, url):
        with pytest.raises(InvalidFundraiserUrlException):
            scraper = MyDonateScraperCreator(url=url).get_scraper()
