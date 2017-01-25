import time


class InvalidDonationException(Exception):
    pass


class Donation:
    def __init__(self, amount, timestamp=int(time.time()), identifier=None, event_identifier=None):
        self._amount = amount
        self._timestamp = timestamp
        self._identifier = identifier
        self._event_identifier = event_identifier
        self.__validate_donation()
        self.__parse_donation_amount()

    def __validate_donation(self):
        if self._amount == '':
            raise InvalidDonationException('Donation amount cannot be an empty string')
        if self._amount == 0:
            raise InvalidDonationException('Donation cannot have a value of 0')
        if self._timestamp < 0:
            raise InvalidDonationException('Invalid timestamp passed')

    def __parse_donation_amount(self):
        if isinstance(self._amount, str):
            self._amount = self._amount.replace(',', '')
            try:
                self._amount = float(self._amount)
            except ValueError:
                raise InvalidDonationException('Cannot parse input string properly')

    @property
    def amount(self):
        return self._amount

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def identifier(self):
        return self._identifier

    @property
    def event_identifier(self):
        return self._event_identifier
