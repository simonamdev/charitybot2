import pytest
import charitybot2.sources.justgiving as justgiving

fundraiser_name = 'Disability-North'


class TestFundraiserValidity:
    # This test might end up being invalid if the fundraiser expires and becomes a 404
    def test_new_valid_fundraiser(self):
        jg = justgiving.JustGivingScraper(fundraiser_name=fundraiser_name, verbose=True)
        assert jg.is_valid is True

    def test_no_fundraiser_name_raises_exception(self):
        with pytest.raises(justgiving.NoFundraiserNameGivenException):
            justgiving.JustGivingScraper()

    def test_invalid_fundraiser_name_given_raises_exception(self):
        with pytest.raises(justgiving.InvalidFundraiserUrlException):
            justgiving.JustGivingScraper(fundraiser_name='isdofjisdjfiojsdfoijo', verbose=True)


class TestFundraiserRetrieve:
    def test_get_amount_raised(self):
        jg = justgiving.JustGivingScraper(fundraiser_name=fundraiser_name, verbose=True)
        amount_raised = jg.get_source_value(source_name='amount_raised')
        # since the amount raised is not static, at least we can check for the £ and decimal point
        assert amount_raised is not None
        assert '£' in amount_raised
        assert '.' in amount_raised
