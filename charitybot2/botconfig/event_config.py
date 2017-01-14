import re

from charitybot2.botconfig.json_config import InvalidConfigurationException, JSONConfigurationFile
from charitybot2.events.currency import InvalidCurrencyException

url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'


class EventConfiguration:
    def __init__(self, config_values):
        self.config_values = config_values

    def get_value(self, key):
        return self.config_values[key]


class EventConfigurationCreator:
    keys_required = (
        'internal_name',
        'external_name',
        'start_time',
        'end_time',
        'currency_key',
        'target_amount',
        'source_url',
        'update_delay'
    )

    number_keys = [
        'start_time',
        'end_time',
        'target_amount',
        'update_delay'
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
        # Test for spaces in Event Name
        if ' ' in self.config_values['internal_name']:
            raise InvalidConfigurationException('Event internal names cannot have spaces')
        # Test that number keys are actually numbers
        for key in self.number_keys:
            if not isinstance(self.config_values[key], int):
                raise InvalidConfigurationException('Expected numbers in key: {} but found something else instead'.format(key))
        # Test that the currency key is recognised
        if self.config_values['currency_key'] not in self.currencies:
            raise InvalidCurrencyException(
                    'Invalid currency key passed. Please use one of the following: {}'.format(
                        str(self.currencies)))
        # Test that the URL actually is a URL
        url_count = re.findall(url_regex, self.config_values['source_url'])
        if not len(url_count) == 1:
            raise InvalidConfigurationException('URL provided in configuration is not a valid URL')
        # Test that the event end time is greater than the start time
        if not self.config_values['end_time'] > self.config_values['start_time']:
            raise InvalidConfigurationException('Event end time is not greater than '
                                                'the event start time. End time: {} Start time: {}'.format(
                                                    self.config_values['end_time'],
                                                    self.config_values['start_time']
                                                ))

    def get_event_configuration(self):
        return EventConfiguration(self.config_values)


class EventConfigurationFromFile(JSONConfigurationFile):
    def __init__(self, file_path):
        super().__init__(file_path=file_path, keys_required=EventConfigurationCreator.keys_required)

    def get_config_data(self):
        return self.config_data

    def get_event_configuration(self):
        return EventConfigurationCreator(config_values=self.config_data).get_event_configuration()
