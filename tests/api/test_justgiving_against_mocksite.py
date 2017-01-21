import pytest
from charitybot2.sources.justgiving import JustGivingScraperCreator
from charitybot2.sources.mocks.mocksite import mock_justgiving_fundraising_url, mock_justgiving_campaign_url, \
    actual_justgiving_campaign_url, actual_justgiving_fundraising_url, mock_justgiving_api_url
from charitybot2.sources.scraper import SourceUnavailableException
from charitybot2.sources.url_call import UrlCall, ConnectionFailedException
from tests.mocks import MockFundraisingWebsite

mock_fundraising_website = MockFundraisingWebsite(fundraiser_name='justgiving')


def try_to_start_mocksite():
    try:
        response = UrlCall(url=mock_fundraising_website.url).get()
        if not response.status_code == 200:
            mock_fundraising_website.start()
    except ConnectionFailedException:
        mock_fundraising_website.start()


def setup_module():
    try_to_start_mocksite()


def teardown_module():
    # Stop the mocksite only if it is still up
    try:
        response = UrlCall(url=mock_fundraising_website.url).get()
        if response.status_code == 200:
            mock_fundraising_website.stop()
    except ConnectionFailedException:
        pass


class TestJustGivingFundraisingScraping:
    def test_get_amount_raised_from_actual_fundraising_url(self):
        jg = JustGivingScraperCreator(
            url=actual_justgiving_fundraising_url,
            debug=True).get_scraper()
        amount_raised = jg.scrape_amount_raised()
        # since the amount raised is not static, at least we can check for the £ and decimal point
        assert amount_raised is not None
        assert '£' in amount_raised
        assert '.' in amount_raised or ',' in amount_raised

    def test_get_amount_raised_from_fundraiser_page(self):
        jg = JustGivingScraperCreator(
            url=mock_justgiving_fundraising_url,
            debug=True).get_scraper()
        amount_raised = jg.scrape_amount_raised()
        assert '£100.52' == amount_raised


class TestJustGivingCampaignScraper:
    def test_get_amount_raised_from_actual_url(self):
        try_to_start_mocksite()
        jg = JustGivingScraperCreator(
            url=actual_justgiving_campaign_url,
            debug=True).get_scraper()
        amount_raised = jg.scrape_amount_raised()
        assert amount_raised is not None
        assert '£' in amount_raised
        assert '.' in amount_raised or ',' in amount_raised

    def test_get_amount_raised_from_campaign_page(self):
        jg = JustGivingScraperCreator(
            url=mock_justgiving_campaign_url,
            debug=True).get_scraper()
        amount_raised = jg.scrape_amount_raised()
        assert '£100.52' == amount_raised


# TODO: Refactor these three above test classes into a parameterised test
class TestJustGivingAPIScraper:
    def test_get_amount_raised_from_actual_url(self):
        pass

    def test_get_amount_raised_from_mock_api(self):
        jg = JustGivingScraperCreator(
            url=mock_justgiving_api_url,
            debug=True).get_scraper()
        amount_raised = jg.scrape_amount_raised()
        assert '100.52' == amount_raised


class TestJustGivingScraperFailure:
    def test_get_amount_raised_fails_gracefully(self):
        try_to_start_mocksite()
        jg = JustGivingScraperCreator(
            url=mock_justgiving_fundraising_url,
            debug=True).get_scraper()
        # simulate as if the website went down
        mock_fundraising_website.stop()
        with pytest.raises(SourceUnavailableException):
            amount_raised = jg.scrape_amount_raised()
