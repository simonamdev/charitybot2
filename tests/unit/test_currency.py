import pytest
from charitybot2.models.currency import Currency


class TestCurrencyInstantiation:
    @pytest.mark.parametrize('key', [
        'GBP',
        'USD',
        'EUR'
    ])
    def test_retrieve_key(self, key):
        currency = Currency(key=key)
        assert key == currency.get_key()

    @pytest.mark.parametrize('key,symbol', [
        ('GBP', '£'),
        ('USD', '$'),
        ('EUR', '€')
    ])
    def test_retrieve_symbol(self, key, symbol):
        currency = Currency(key=key)
        assert symbol == currency.get_symbol()
