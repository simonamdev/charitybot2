from charitybot2.botconfig.json_config import JSONConfigurationFile, InvalidConfigurationException
from charitybot2.events.currency import InvalidCurrencyException


class InvalidEventNameException(Exception):
    pass


class EventConfiguration(JSONConfigurationFile):
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

    def __init__(self, file_path):
        super().__init__(file_path=file_path, keys_required=self.keys_required)

    def run_extra_validation(self):
        if self.config_data['currency'] not in self.currencies:
            raise InvalidCurrencyException('Provided currency is invalid.'
                                           ' Please use any of the following: {}'.format(self.currencies))
        if ' ' in self.config_data['event_name']:
            raise InvalidEventNameException('Event names cannot have spaces within them. Use underscores instead!')


class EventConfigurationCreator:
    def __init__(self, config_values):
        self.config_values = config_values
        self.validate_keys_passed()
        self.validate_key_types()

    def validate_keys_passed(self):
        if not sorted(list(self.config_values.keys())) == sorted(EventConfiguration.keys_required):
            raise InvalidConfigurationException

    def validate_key_types(self):
        for key in EventConfiguration.number_keys:
            if not isinstance(self.config_values[key], int):
                raise InvalidConfigurationException
        if self.config_values['currency'] not in EventConfiguration.currencies:
            raise InvalidConfigurationException
