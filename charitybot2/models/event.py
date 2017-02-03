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
