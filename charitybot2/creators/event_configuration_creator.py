import re
from charitybot2.configurations.event_configuration import EventConfiguration
from charitybot2.models.currency import InvalidCurrencyKeyException


class InvalidEventConfigurationException(Exception):
    pass


class EventConfigurationCreator:
    _keys_required = (
        'identifier',
        'title',
        'start_time',
        'end_time',
        'currency_key',
        'target_amount',
        'source_url',
        'update_delay'
    )

    _number_keys = (
        'start_time',
        'end_time',
        'target_amount',
        'update_delay'
    )

    _url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

    def __init__(self, configuration_values):
        self._configuration_values = configuration_values
        self._configuration = None
        self.__validate_configuration_values_passed()
        self.__create_configuration()
        self.__validate_created_configuration()

    def __validate_configuration_values_passed(self):
        if not isinstance(self._configuration_values, dict):
            raise InvalidEventConfigurationException('Configuration Values must be a Dictionary')
        if self._configuration_values == {}:
            raise InvalidEventConfigurationException('Configuration Values Dictionary cannot be empty')
        if not sorted(self._configuration_values.keys()) == sorted(self._keys_required):
            raise InvalidEventConfigurationException('Passed Configuration keys are incorrect')
        for key in self._number_keys:
            if not isinstance(self._configuration_values[key], int):
                raise InvalidEventConfigurationException('Number keys are required to be integers')

    def __create_configuration(self):
        try:
            self._configuration = EventConfiguration(configuration_values=self._configuration_values)
            key = self._configuration.currency  # check for currency validity
        except InvalidCurrencyKeyException:
            raise InvalidEventConfigurationException('Invalid currency key passed')

    def __validate_created_configuration(self):
        if self._configuration.end_time < self._configuration.start_time:
            raise InvalidEventConfigurationException('Start time cannot be after end time')
        if self._configuration.start_time < 0 or self._configuration.end_time < 0:
            raise InvalidEventConfigurationException('Time values cannot be negative or less than zero')
        if ' ' in self._configuration.identifier:
            raise InvalidEventConfigurationException('Identifiers cannot have spaces')
        if self._configuration.identifier == '' or self._configuration.title == '':
            raise InvalidEventConfigurationException('Identifier and/or title cannot be empty')
        url_count = re.findall(self._url_regex, self._configuration.source_url)
        if not len(url_count) == 1:
            raise InvalidEventConfigurationException('Source URL is not actually a URL')

    @property
    def configuration(self):
        return self._configuration
