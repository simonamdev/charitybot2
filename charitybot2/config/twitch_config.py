from charitybot2.config.json_config import JSONConfigurationFile


class TwitchAccountConfiguration(JSONConfigurationFile):
    keys_required = (
        'name',
        'id',
        'secret'
    )

    def __init__(self, file_path):
        super().__init__(file_path=file_path, keys_required=self.keys_required)

    def get_account_name(self):
        return self.config_data['name']

    def get_client_id(self):
        return self.config_data['id']

    def get_client_secret(self):
        return self.config_data['secret']
