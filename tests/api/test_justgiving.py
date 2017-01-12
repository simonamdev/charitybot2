import pytest
from charitybot2.paths import mocksite_path
from charitybot2.sources.justgiving import JustGivingScraper
from charitybot2.sources.scraper import SourceUnavailableException
from tests.integration.test_event_loop_with_mocksite import MockEvent
from tests.tests import ServiceTest

mocksite = ServiceTest(
    service_name='Donations Mocksite',
    service_url=MockEvent.mocksite_base_url,
    service_path=mocksite_path,
    enter_debug=False)


class TestFundraiserRetrieve:
    def test_get_amount_raised_from_mocksite(self):
        mocksite.start_service()
        jg = JustGivingScraper(url=MockEvent.mocksite_base_url + 'justgiving/', debug=True)
        amount_raised = jg.get_source_value(source_name='amount_raised')
        assert '£100.52' == amount_raised
        mocksite.stop_service()

    def test_get_amount_raised_from_actual_url(self):
        jg = JustGivingScraper(url='https://www.justgiving.com/fundraising/alasdair-clift', debug=True)
        amount_raised = jg.get_source_value(source_name='amount_raised')
        # since the amount raised is not static, at least we can check for the £ and decimal point
        assert amount_raised is not None
        assert '£' in amount_raised
        assert '.' in amount_raised or ',' in amount_raised

    def test_get_amount_raised_fails_gracefully(self):
        mocksite.start_service()
        jg = JustGivingScraper(url=MockEvent.mocksite_base_url, debug=True)
        # simulate as if the website went down
        mocksite.stop_service()
        with pytest.raises(SourceUnavailableException):
            amount_raised = jg.scrape_amount_raised()
