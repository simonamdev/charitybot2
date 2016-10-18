import pytest

from charitybot2.events.donation import Donation, InvalidArgumentException


class TestDonationValidity:
    def test_passing_empty_amounts_throws_exception(self):
        with pytest.raises(InvalidArgumentException):
            Donation('', '')

    def test_passing_first_amount_empty_throws_exception(self):
        with pytest.raises(InvalidArgumentException):
            Donation('', '25.4')

    def test_passing_second_amount_empty_throws_exception(self):
        with pytest.raises(InvalidArgumentException):
            Donation('33.3', '')

    def test_passing_smaller_new_amount_throws_exception(self):
        with pytest.raises(InvalidArgumentException):
            Donation(old_amount='33.3', new_amount='22.2')


class TestDonationProcessing:
    def test_passing_valid_inputs_is_ok(self):
        donation = Donation(old_amount='33.3', new_amount='55.5')
        assert isinstance(donation, Donation)

    def test_passing_currency_symbols_processes_normally(self):
        donation = Donation(old_amount='£50', new_amount='£100')
        assert donation.get_donation_amount() == 50

    def test_passing_commas_and_decimal_points_processes_normally(self):
        donation = Donation(old_amount='5000.32', new_amount='7,000.52')
        assert donation.get_donation_amount() == 2000

    def test_passing_all_symbols_processes_normally(self):
        donation = Donation(old_amount='$3,000.33', new_amount='$30,010.55')
        assert donation.get_donation_amount() == 27010
