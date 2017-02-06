class InvalidCurrencyException(Exception):
    pass


class Currency:
    GBP = '£'
    USD = '$'
    EUR = '€'
    symbols = [GBP, USD, EUR]
    keys = ['GBP', 'USD', 'EUR']
    symbol_map = {
        'GBP': GBP,
        'USD': USD,
        'EUR': EUR
    }

    def __init__(self, key='GBP'):
        self.key = key
        self.validate_key()

    def validate_key(self):
        if self.key not in self.keys:
            raise InvalidCurrencyException

    def get_symbol(self):
        return self.symbol_map[self.key]

    def get_key(self):
        return self.key
