import json

from charitybot2.models.currency import Currency


class EventConfiguration:
    def __init__(self, configuration_values=None):
        self._configuration_values = configuration_values

    def __str__(self):
        return json.dumps(self._configuration_values)

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

    @property
    def source_url(self):
        return self._configuration_values['source_details']['url']

    @property
    def configuration_values(self):
        return self._configuration_values
