import pytest

from charitybot2.events.donation import Donation, InvalidArgumentException


class TestDonationValidity:
    @pytest.mark.parametrize('old_amount,new_amount', [
        ('',     ''),
        ('',     '25.4'),
        ('33.3', '')
    ])
    def test_passing_invalid_amounts_throws_exception(self, old_amount, new_amount):
        with pytest.raises(InvalidArgumentException):
            Donation(old_amount=old_amount, new_amount=new_amount)

    def test_passing_smaller_new_amount_throws_exception(self):
        with pytest.raises(InvalidArgumentException):
            Donation(old_amount='33.3', new_amount='22.2')

    def test_passing_smaller_new_amount_invalid_donation_does_not_throw_exception(self):
        Donation(old_amount='33.3', new_amount='22.2', valid=False)

    def test_passing_floats_processes_normally(self):
        donation = Donation(old_amount=33.3, new_amount=44.4)
        assert 11.1 == donation.get_donation_amount()


class TestDonationAttributes:
    def test_passing_valid_inputs_is_ok(self):
        donation = Donation(old_amount='33.3', new_amount='55.5')
        assert isinstance(donation, Donation)

    @pytest.mark.parametrize('expected_output,actual_output', [
        (Donation('£50', '£100').get_donation_amount(), 50),
        (Donation('5000.32', '7,000.52').get_donation_amount(), 2000.20),
        (Donation(old_amount='$3,000.33', new_amount='$30,010.55').get_donation_amount(), 27010.22),
        (Donation(old_amount='$3,000.33', new_amount='$30,010.55', timestamp=5).get_timestamp(), 5),
        (Donation(old_amount=0, new_amount=1, timestamp=5.23).get_timestamp(), 5),
        (Donation(old_amount=0, new_amount=1, notes='much test very driven').get_notes(), 'much test very driven'),
        (Donation(old_amount=0, new_amount=1, valid=False).get_validity(), False),
        (Donation(old_amount=0, new_amount=1).get_notes(), ''),
        (Donation(old_amount=0, new_amount=1).get_validity(), True)
    ])
    def test_getting_donation_information_when_passing_varying_valid_input(self, expected_output, actual_output):
        assert expected_output == actual_output
