import pytest
import justgiving


def test_always_passes():
    assert True is True

fundraiser_name = 'Disability-North'


# This test might end up being invalid if the fundraiser expires and becomes a 404
def test_new_valid_fundraiser():
    print(fundraiser_name)
    jg = justgiving.JustGivingScraper(fundraiser_name=fundraiser_name, verbose=True)
    assert jg.is_valid is True


def test_no_fundraiser_name_raises_exception():
    with pytest.raises(justgiving.NoFundraiserNameGivenException):
        justgiving.JustGivingScraper()


def test_invalid_fundraiser_name_given_raises_exception():
    with pytest.raises(justgiving.InvalidFundraiserUrlException):
        justgiving.JustGivingScraper(fundraiser_name='isdofjisdjfiojsdfoijo', verbose=True)


def test_get_amount_raised():
    jg = justgiving.JustGivingScraper(fundraiser_name=fundraiser_name, verbose=True)

