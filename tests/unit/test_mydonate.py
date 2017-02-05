import pytest
from charitybot2.sources.mocks.mocksite import mock_mydonate_teams_url, actual_mydonate_teams_url
from charitybot2.sources.mydonate import MyDonateScraperCreator, MyDonateTeamsScraper
from charitybot2.sources.scraper import InvalidFundraiserUrlException


class TestMydonateScraperCreation:
    @pytest.mark.parametrize('url', {
        '',
        'http://www.mydonate.com/blablalbal'
    })
    def test_creating_with_invalid_url_throws_exception(self, url):
        with pytest.raises(InvalidFundraiserUrlException):
            scraper = MyDonateScraperCreator(url=url).get_scraper()

    @pytest.mark.parametrize('url,expected_type,expected_class', [
        (mock_mydonate_teams_url,   'team', MyDonateTeamsScraper),
        (actual_mydonate_teams_url, 'team', MyDonateTeamsScraper)
    ])
    def test_receiving_expected_scraper_type(self, url, expected_type, expected_class):
        scraper = MyDonateScraperCreator(url=url, debug=True).get_scraper()
        assert isinstance(scraper, expected_class)
        assert expected_type == scraper.get_type()
