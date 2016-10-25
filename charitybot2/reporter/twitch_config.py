class IllegalConfigValueException(Exception):
    pass


class TwitchConfig:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.validate_parameters()

    def validate_parameters(self):
        if self.client_id == '' or self.client_secret == '':
            raise IllegalConfigValueException

    def get_client_id(self):
        return self.client_id

    def get_client_secret(self):
        return self.client_secret
