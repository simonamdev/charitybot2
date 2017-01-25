class InvalidCurrencyKeyException(Exception):
    pass


class Currency:
    __currency_symbol_lookup = {
        'GBP': '£',
        'USD': '$',
        'EUR': '€'
    }

    def __init__(self, key):
        self._key = key
        self.__validate_key()

    def __validate_key(self):
        if self._key not in self.__currency_symbol_lookup.keys():
            raise InvalidCurrencyKeyException('Given key: {} is not a valid currency key'.format(self._key))

    @property
    def key(self):
        return self._key

    @property
    def symbol(self):
        return self.__currency_symbol_lookup[self._key]
