class InvalidEventAmountException(Exception):
    pass


class Event:
    def __init__(self, configuration):
        self._configuration = configuration
        self._starting_amount = 0
        self._amount_raised = 0

    @property
    def configuration(self):
        return self._configuration

    @property
    def starting_amount(self):
        return self._starting_amount

    @property
    def amount_raised(self):
        return self._amount_raised

    @staticmethod
    def __verify_amount_passed(amount):
        if not type(amount) in (int, float):
            raise InvalidEventAmountException('Amount is not a number')
        if amount < 0:
            raise InvalidEventAmountException('Amount cannot be negative')

    def set_starting_amount(self, starting_amount):
        self.__verify_amount_passed(amount=starting_amount)
        self._starting_amount = starting_amount

    def set_amount_raised(self, amount_raised):
        self.__verify_amount_passed(amount=amount_raised)
        self._amount_raised = amount_raised

