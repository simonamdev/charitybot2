from charitybot2.models.currency import Currency


class EventConfiguration:
    def __init__(self, configuration_values=None):
        self._configuration_values = configuration_values

    @property
    def identifier(self):
        return self._configuration_values['identifier']

    @property
    def title(self):
        return self._configuration_values['title']

    @property
    def start_time(self):
        return self._configuration_values['start_time']

    @property
    def end_time(self):
        return self._configuration_values['end_time']

    @property
    def target_amount(self):
        return self._configuration_values['target_amount']

    @property
    def update_delay(self):
        return self._configuration_values['update_delay']

    @property
    def currency(self):
        return Currency(key=self._configuration_values['currency_key'])
