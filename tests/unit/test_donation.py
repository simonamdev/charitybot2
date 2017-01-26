import pytest
import time
from charitybot2.models.donation import Donation, InvalidDonationException

test_donation = Donation(
    amount=50,
    timestamp=999999,
    identifier='identifier',
    event_identifier='event_identifier',
    notes='Automated')


class TestDonationInstantiation:
    @pytest.mark.parametrize('expected,actual', [
        (50, test_donation.amount),
        (999999, test_donation.timestamp),
        ('identifier', test_donation.identifier),
        ('event_identifier', test_donation.event_identifier),
        ('Automated', test_donation.notes),
        (True, test_donation.validity)
    ])
    def test_retrieval(self, expected, actual):
        assert expected == actual

    @pytest.mark.parametrize('amount', [
        '12345.67',
        '12,345.67',
        '1234,5.67',
        '1,2345.67'
    ])
    def test_passing_amount_string_with_commas_parses_properly(self, amount):
        donation = Donation(amount=amount, timestamp=0)
        assert 12345.67 == donation.amount

    @pytest.mark.parametrize('amount', [
        123.45,
        123.454,
        123.4543,
        123.45432
    ])
    def test_donation_amount_rounding(self, amount):
        donation = Donation(amount=amount)
        assert 123.45 == donation.amount

    def test_donation_defaults(self):
        donation = Donation(amount=1)
        assert 1 == donation.amount
        assert int(time.time()) + 2 >= donation.timestamp >= int(time.time()) - 2
        assert None is donation.identifier
        assert None is donation.event_identifier
        assert None is donation.notes
        assert True is donation.validity


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
