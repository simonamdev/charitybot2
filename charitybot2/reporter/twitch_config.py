class IllegalConfigValueException(Exception):
    pass


class TwitchConfig:
    def __init__(self, account_name, client_id, client_secret):
        self.account_name = account_name
        self.client_id = client_id
        self.client_secret = client_secret
        self.validate_parameters()

    def validate_parameters(self):
        if self.client_id == '' or self.client_secret == '' or self.account_name == '':
            raise IllegalConfigValueException

    def get_account_name(self):
        return self.account_name

    def get_client_id(self):
        return self.client_id

    def get_client_secret(self):
        return self.client_secret
