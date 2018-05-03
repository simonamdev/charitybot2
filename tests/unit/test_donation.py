import json

import pytest
import time
from charitybot2.models.donation import Donation, InvalidDonationException

test_donation_amount = 50
test_donation_event_identifier = 'event_identifier'
test_donation_timestamp = 999999
test_donation_currency_code = 'TEST'
test_donation_internal_reference = 'internal_reference'
test_donation_external_reference = 'external_reference'
test_donation_notes = 'Automated'
test_donation_donor_name = 'donor'

test_donation = Donation(
    amount=test_donation_amount,
    event_identifier=test_donation_event_identifier,
    currency_code=test_donation_currency_code,
    timestamp=test_donation_timestamp,
    internal_reference=test_donation_internal_reference,
    external_reference=test_donation_external_reference,
    donor_name=test_donation_donor_name,
    notes=test_donation_notes)


class TestDonationInstantiation:
    @pytest.mark.parametrize('expected,actual', [
        (test_donation_amount, test_donation.amount),
        (test_donation_event_identifier, test_donation.event_identifier),
        (test_donation_timestamp, test_donation.timestamp),
        (test_donation_currency_code, test_donation.currency_code),
        (test_donation_internal_reference, test_donation.internal_reference),
        (test_donation_external_reference, test_donation.external_reference),
        (test_donation_donor_name, test_donation.donor_name),
        (test_donation_notes, test_donation.notes),
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
        donation = Donation(
            amount=amount,
            event_identifier=test_donation_event_identifier,
            currency_code=test_donation_currency_code)
        assert 12345.67 == donation.amount

    @pytest.mark.parametrize('amount', [
        123.45,
        123.454,
        123.4543,
        123.45432
    ])
    def test_donation_amount_rounding(self, amount):
        donation = Donation(
            amount=amount,
            event_identifier=test_donation_event_identifier,
            currency_code=test_donation_currency_code)
        assert 123.45 == donation.amount

    def test_donation_optional_defaults(self):
        donation = Donation(
            amount=1,
            event_identifier=test_donation_event_identifier,
            currency_code=test_donation_currency_code)
        assert int(time.time()) + 2 >= donation.timestamp >= int(time.time()) - 2
        assert None is donation.notes
        assert True is donation.validity

    def test_two_donations_have_different_internal_references(self):
        donation_one = Donation(
            amount=1,
            event_identifier=test_donation_event_identifier,
            currency_code=test_donation_currency_code)
        donation_two = Donation(
            amount=2,
            event_identifier=test_donation_event_identifier,
            currency_code=test_donation_currency_code)
        assert not donation_one.internal_reference == donation_two.internal_reference


class TestDonationExceptions:
    @pytest.mark.parametrize('amount,timestamp,event_identifier,internal_reference', [
        (None, 0, 'event', 'bla'),
        (0, 0, 'event', 'bla'),
        (1, 0, None, 'bla'),
        (test_donation_amount, -20, None, 'bla'),
        ('', 0, None, 'bla'),
        ('foobar', 0, None, 'bla'),
        (1, 0, 'event', 1.234)
    ])
    def test_incorrect_values_throws_exception(self, amount, timestamp, event_identifier, internal_reference):
        with pytest.raises(InvalidDonationException):
            Donation(
                amount=amount,
                event_identifier=event_identifier,
                currency_code=test_donation_currency_code,
                timestamp=timestamp,
                internal_reference=internal_reference)


class TestDonationMethods:
    test_donation_dict = dict(
        amount=test_donation.amount,
        event_identifier=test_donation.event_identifier,
        currency_code=test_donation_currency_code,
        timestamp=test_donation.timestamp,
        internal_reference=test_donation.internal_reference,
        external_reference=test_donation.external_reference,
        donor_name=test_donation_donor_name,
        notes=test_donation.notes,
        valid=test_donation.validity)

    def test_conversion_from_valid_dict(self):
        donation = Donation.from_dict(self.test_donation_dict)
        assert test_donation.amount == donation.amount
        assert test_donation.event_identifier == donation.event_identifier
        assert test_donation.currency_code == donation.currency_code
        assert test_donation.timestamp == donation.timestamp
        assert test_donation.internal_reference == donation.internal_reference
        assert test_donation.external_reference == donation.external_reference
        assert test_donation.donor_name == donation.donor_name
        assert test_donation.notes == donation.notes
        assert test_donation.validity == donation.validity

    @pytest.mark.parametrize('donation_dict', [
        dict(),
        dict(foo='bar'),
        dict(amount='-3945'),
        dict(valid=None),
        None,
        1,
        2.0,
        object,
        ''
    ])
    def test_conversion_from_invalid_dict_throws_exception(self, donation_dict):
        with pytest.raises(InvalidDonationException):
            donation = Donation.from_dict(donation_dict=donation_dict)

    def test_conversion_from_valid_json(self):
        donation_json = json.dumps(self.test_donation_dict)
        donation = Donation.from_json(donation_json=donation_json)
        assert test_donation.amount == donation.amount
        assert test_donation.event_identifier == donation.event_identifier
        assert test_donation.currency_code == donation.currency_code
        assert test_donation.timestamp == donation.timestamp
        assert test_donation.internal_reference == donation.internal_reference
        assert test_donation.notes == donation.notes
        assert test_donation.validity == donation.validity

    @pytest.mark.parametrize('donation_json', [
        '',
        'bla',
        '{}',
        '[]',
        'foobarr',
        '{"something" : "or other"}',
        '{"amount": 9001}'
    ])
    def test_conversion_from_invalid_json_throws_exception(self, donation_json):
        with pytest.raises(InvalidDonationException):
            donation = Donation.from_json(donation_json=donation_json)

    def test_conversion_to_dict(self):
        assert self.test_donation_dict == test_donation.to_dict()

    def test_conversion_to_json(self):
        test_donation_json = json.dumps(self.test_donation_dict)
        assert test_donation_json == test_donation.to_json()
