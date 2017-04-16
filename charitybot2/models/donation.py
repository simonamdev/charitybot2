import time


class InvalidDonationException(Exception):
    pass


class Donation:
    __rounding_amount = 2

    def __init__(self,
                 amount,
                 event_identifier,
                 timestamp=int(time.time()),
                 identifier=None,
                 notes=None,
                 valid=True):
        self._amount = amount
        self._event_identifier = event_identifier
        self._timestamp = timestamp
        self._identifier = identifier
        self._notes = notes
        self._valid = valid
        self.__validate_donation()
        self.__parse_donation_amount()

    def __validate_donation(self):
        if self._amount == '':
            raise InvalidDonationException('Donation amount cannot be an empty string')
        if not isinstance(self._event_identifier, str) or self._event_identifier == '':
            raise InvalidDonationException('Invalid Event identifier passed')
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
        self._amount = round(self._amount, self.__rounding_amount)

    @property
    def amount(self):
        return self._amount

    @property
    def event_identifier(self):
        return self._event_identifier

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def identifier(self):
        return self._identifier

    @property
    def notes(self):
        return self._notes

    @property
    def validity(self):
        return self._valid
