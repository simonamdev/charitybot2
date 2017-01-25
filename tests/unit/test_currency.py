import pytest
from charitybot2.models.currency import Currency, InvalidCurrencyKeyException


class TestCurrencyInstantiation:
    @pytest.mark.parametrize('key', [
        'GBP',
        'USD',
        'EUR'
    ])
    def test_retrieve_key(self, key):
        currency = Currency(key=key)
        assert key == currency.key

    @pytest.mark.parametrize('key,symbol', [
        ('GBP', '£'),
        ('USD', '$'),
        ('EUR', '€')
    ])
    def test_retrieve_symbol(self, key, symbol):
        currency = Currency(key=key)
        assert symbol == currency.symbol


class TestCurrencyExceptions:
    @pytest.mark.parametrize('key', [
        '',
        'bla',
        'foo'
    ])
    def test_passing_invalid_key_throws_exception(self, key):
        with pytest.raises(InvalidCurrencyKeyException):
            currency = Currency(key=key)
