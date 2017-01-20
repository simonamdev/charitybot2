import pytest
from charitybot2.sources.justgiving import JustGivingScraperCreator, JustGivingFundraisingScraper, \
    JustGivingCampaignScraper, InvalidFundraiserUrlException
from charitybot2.sources.mocks.mocksite import mock_justgiving_fundraising_url, mock_justgiving_campaign_url


class TestJustGivingScraperCreation:
    def test_creating_with_invalid_url_throws_exception(self):
        with pytest.raises(InvalidFundraiserUrlException):
            scraper = JustGivingScraperCreator(url='http://www.justgiving.com/blalbalbalbla').get_scraper()

    def test_receiving_fundraising_scraper(self):
        scraper = JustGivingScraperCreator(url=mock_justgiving_fundraising_url).get_scraper()
        assert isinstance(scraper, JustGivingFundraisingScraper)
        assert 'fundraising' == scraper.get_type()

    def test_receiving_campaign_scraper(self):
        scraper = JustGivingScraperCreator(url=mock_justgiving_campaign_url).get_scraper()
        assert isinstance(scraper, JustGivingCampaignScraper)
        assert 'campaign' == scraper.get_type()
