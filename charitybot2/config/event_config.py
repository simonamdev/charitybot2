from charitybot2.config.json_config import JSONConfigurationFile


class EventConfiguration(JSONConfigurationFile):
    config_format = 'JSON'
    keys_required = (
        'name',
        'start_time',
        'end_time',
        'target_amount',
        'source_url',
        'update_tick'
    )

    number_keys = [
        'start_time',
        'end_time',
        'target_amount',
        'update_tick'
    ]

    def __init__(self, file_path):
        super().__init__(file_path=file_path, keys_required=self.keys_required)
