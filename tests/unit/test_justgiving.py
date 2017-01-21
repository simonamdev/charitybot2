import pytest
from charitybot2.sources.justgiving import JustGivingScraperCreator, JustGivingFundraisingScraper, \
    JustGivingCampaignScraper, InvalidFundraiserUrlException, JustGivingAPIScraper
from charitybot2.sources.mocks.mocksite import mock_justgiving_fundraising_url, mock_justgiving_campaign_url, \
    mock_justgiving_api_url, actual_justgiving_api_url, actual_justgiving_campaign_url, \
    actual_justgiving_fundraising_url


class TestJustGivingScraperCreation:
    @pytest.mark.parametrize('url,except_expected', [
        ('', InvalidFundraiserUrlException),
        ('http://www.justgiving.com/blablalbal', InvalidFundraiserUrlException)
    ])
    def test_creating_with_invalid_url_throws_exception(self, url, except_expected):
        with pytest.raises(except_expected):
            scraper = JustGivingScraperCreator(url=url).get_scraper()

    @pytest.mark.parametrize('url,expected_type,expected_class', [
        (mock_justgiving_fundraising_url,   'fundraising', JustGivingFundraisingScraper),
        (mock_justgiving_campaign_url,      'campaign',    JustGivingCampaignScraper),
        (mock_justgiving_api_url,           'api',         JustGivingAPIScraper),
        (actual_justgiving_fundraising_url, 'fundraising', JustGivingFundraisingScraper),
        (actual_justgiving_campaign_url,    'campaign',    JustGivingCampaignScraper),
        (actual_justgiving_api_url,         'api',         JustGivingAPIScraper)
    ])
    def test_receiving_expected_mock_fundraising_scraper_type(self, url, expected_type, expected_class):
        scraper = JustGivingScraperCreator(url=url).get_scraper()
        assert isinstance(scraper, expected_class)
        assert expected_type == scraper.get_type()
