import pytest
import charitybot2.sources.justgiving as justgiving

fundraiser_name = 'Disability-North'


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
