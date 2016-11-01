from charitybot2.config.json_config import JSONConfigurationFile


class InvalidCurrencyException(Exception):
    pass


class EventConfiguration(JSONConfigurationFile):
    keys_required = (
        'name',
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

