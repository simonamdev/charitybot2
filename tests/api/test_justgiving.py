import pytest
from charitybot2.sources.justgiving import JustGivingScraper
from charitybot2.sources.scraper import SourceUnavailableException
from tests.integration.test_event_loop_with_mocksite import MockEvent
from tests.mocks import MockFundraisingWebsite

mock_fundraising_website = MockFundraisingWebsite(fundraiser_name='justgiving')


class TestFundraiserRetrieve:
    def test_get_amount_raised_from_actual_url(self):
        jg = JustGivingScraper(url='https://www.justgiving.com/fundraising/alasdair-clift', debug=True)
        amount_raised = jg.get_source_value(source_name='amount_raised')
        # since the amount raised is not static, at least we can check for the £ and decimal point
        assert amount_raised is not None
        assert '£' in amount_raised
        assert '.' in amount_raised or ',' in amount_raised

    def test_get_amount_raised_from_mocksite(self):
        mock_fundraising_website.start()
        jg = JustGivingScraper(url=MockEvent.mocksite_base_url + 'justgiving/', debug=True)
        amount_raised = jg.get_source_value(source_name='amount_raised')
        assert '£100.52' == amount_raised
        mock_fundraising_website.stop()

    def test_get_amount_raised_fails_gracefully(self):
        mock_fundraising_website.start()
        jg = JustGivingScraper(url=MockEvent.mocksite_base_url, debug=True)
        # simulate as if the website went down
        mock_fundraising_website.stop()
        with pytest.raises(SourceUnavailableException):
            amount_raised = jg.scrape_amount_raised()
