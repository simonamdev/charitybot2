import pytest
from charitybot2.models.donation import Donation, InvalidDonationException

test_donation = Donation(
    amount=50,
    timestamp=999999,
    identifier='identifier',
    event_identifier='event_identifier')


class TestDonationInstantiation:
    @pytest.mark.parametrize('expected,actual', [
        (50, test_donation.amount),
        (999999, test_donation.timestamp),
        ('identifier', test_donation.identifier),
        ('event_identifier', test_donation.event_identifier)
    ])
    def test_retrieval(self, expected, actual):
        assert expected == actual

    def test_passing_amount_string_with_commas_parses_properly(self):
        donation_amount = '12,345.52'
        donation = Donation(amount=donation_amount, timestamp=0)
        assert 12345.52 == donation.amount


class TestDonationExceptions:
    @pytest.mark.parametrize('amount,timestamp,identifier,event_identifier', [
        (0, 0, None, None),
        (50, -20, None, None),
        ('', 0, None, None),
        ('foobar', 0, None, None)
    ])
    def test_incorrect_values_throws_exception(self, amount, timestamp, identifier, event_identifier):
        with pytest.raises(InvalidDonationException):
            Donation(amount=amount, timestamp=timestamp, identifier=identifier, event_identifier=event_identifier)
