import re

from charitybot2.botconfig.json_config import InvalidConfigurationException
from charitybot2.events.currency import InvalidCurrencyException

url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'


class EventConfiguration:
    def __init__(self, config_values):
        self.config_values = config_values


class EventConfigurationCreator:
    keys_required = (
        'event_name',
        'channel_name',
        'start_time',
        'end_time',
        'target_amount',
        'currency',
        'source_url',
        'update_tick'
    )

    number_keys = [
        'start_time',
        'end_time',
        'target_amount',
        'update_tick'
    ]

    currencies = (
        'USD',
        'GBP',
        'EUR'
    )

    def __init__(self, config_values):
        self.config_values = config_values
        self.validate_keys_passed()
        self.validate_key_types()

    def validate_keys_passed(self):
        if not sorted(list(self.config_values.keys())) == sorted(self.keys_required):
            raise InvalidConfigurationException('Keys provided do not match keys required for event configuration')

    def validate_key_types(self):
        if ' ' in self.config_values['event_name']:
            raise InvalidConfigurationException('Currently event names cannot have spaces, use underscores')
        for key in self.number_keys:
            if not isinstance(self.config_values[key], int):
                raise InvalidConfigurationException('Expected numbers in key: {} but found something else instead'.format(key))
        if self.config_values['currency'] not in self.currencies:
            raise InvalidCurrencyException(
                    'Invalid currency key passed. Please use one of the following: {}'.format(
                        str(self.currencies)))
        url_count = re.findall(url_regex, self.config_values['source_url'])
        if not len(url_count) == 1:
            raise InvalidConfigurationException('URL provided in configuration is not a valid URL')

    def get_event_configuration(self):
        return EventConfiguration(self.config_values)
