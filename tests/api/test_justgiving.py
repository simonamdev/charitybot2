import pytest
import charitybot2.sources.justgiving as justgiving
from charitybot2.paths import mocksite_path
from charitybot2.sources.scraper import SourceUnavailableException
from tests.integration.test_event_loop_with_mocksite import MockEvent
from tests.tests import ServiceTest

fundraiser_name = 'Disability-North'

service_test = ServiceTest(
    service_name='Donations Mocksite',
    service_url=MockEvent.mocksite_base_url,
    service_path=mocksite_path,
    enter_debug=False)


class TestFundraiserValidity:
    def test_invalid_fundraiser_name_given_raises_exception(self):
        with pytest.raises(justgiving.InvalidFundraiserUrlException):
            justgiving.JustGivingScraper(url='isdofjisdjfiojsdfoijo', verbose=True)


class TestFundraiserRetrieve:
    def test_get_amount_raised(self):
        jg = justgiving.JustGivingScraper(url='https://www.justgiving.com/fundraising/alasdair-clift', verbose=True)
        amount_raised = jg.get_source_value(source_name='amount_raised')
        # since the amount raised is not static, at least we can check for the £ and decimal point
        assert amount_raised is not None
        assert '£' in amount_raised
        assert '.' in amount_raised or ',' in amount_raised

    def test_get_amount_raised_fails_gracefully(self):
        service_test.start_service()
        jg = justgiving.JustGivingScraper(url=MockEvent.mocksite_base_url, verbose=True)
        # simulate as if the website went down
        service_test.stop_service()
        with pytest.raises(SourceUnavailableException):
            amount_raised = jg.get_amount_raised()
