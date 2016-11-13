import pytest
from charitybot2.events.currency import InvalidCurrencyException, Currency


class TestInitialiseCurrency:
    def test_currency_object_with_non_existent_currency_throws_exception(self):
        with pytest.raises(InvalidCurrencyException):
            currency = Currency(key='Bla')

    def test_default_currency_is_gbp(self):
        currency = Currency()
        assert Currency.GBP == currency.get_symbol()

    def test_return_given_key(self):
        currency = Currency(key='USD')
        assert 'USD' == currency.get_key()
