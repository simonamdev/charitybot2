from urllib.parse import urljoin

import pytest
from charitybot2.sources.justgiving import JustGivingScraper
from charitybot2.sources.scraper import SourceUnavailableException
from charitybot2.sources.url_call import UrlCall, ConnectionFailedException
from tests.integration.test_event_loop_with_mocksite import MockEvent
from tests.mocks import MockFundraisingWebsite

mock_fundraising_website = MockFundraisingWebsite(fundraiser_name='justgiving')


def setup_module():
    mock_fundraising_website.start()


def teardown_module():
    # Stop the mocksite only if it is still up
    try:
        response = UrlCall(url=mock_fundraising_website.url).get()
        if response.status_code == 200:
            mock_fundraising_website.stop()
    except ConnectionFailedException:
        pass


class TestFundraiserRetrieve:
    def test_get_amount_raised_from_actual_url(self):
        jg = JustGivingScraper(url='https://www.justgiving.com/fundraising/alasdair-clift', debug=True)
        amount_raised = jg.get_source_value(source_name='amount_raised')
        # since the amount raised is not static, at least we can check for the £ and decimal point
        assert amount_raised is not None
        assert '£' in amount_raised
        assert '.' in amount_raised or ',' in amount_raised

    def test_get_amount_raised_from_fundraiser_page(self):
        jg = JustGivingScraper(url=MockEvent.mocksite_base_url + 'justgiving/', debug=True)
        amount_raised = jg.get_source_value(source_name='amount_raised')
        assert '£100.52' == amount_raised

    def test_get_amount_raised_from_campaign_page(self):
        jg = JustGivingScraper(url=urljoin(MockEvent.mocksite_base_url, '/justgiving/campaign'), debug=True)
        amount_raised = jg.get_source_value(source_name='amount_raised')
        assert '£100.52' == amount_raised

    def test_get_amount_raised_fails_gracefully(self):
        # only start  the mocksite if it is not running
        if not UrlCall(url=mock_fundraising_website.url).get().status_code == 200:
            mock_fundraising_website.start()
        jg = JustGivingScraper(url=MockEvent.mocksite_base_url, debug=True)
        # simulate as if the website went down
        mock_fundraising_website.stop()
        with pytest.raises(SourceUnavailableException):
            amount_raised = jg.scrape_amount_raised()
