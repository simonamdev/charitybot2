source_names_supported = [
    'justgiving',
    'btdonate'
]


class InvalidSourceNameException(Exception):
    pass


class EmptySourceArgumentException(Exception):
    pass


class Source:
    def __init__(self, name, url_name):
        self.name = name
        self.url_name = url_name
        self.validate_source()

    def validate_source(self):
        if self.name == '' or self.url_name == '':
            raise EmptySourceArgumentException
        if self.name not in source_names_supported:
            raise InvalidSourceNameException

    def get_name(self):
        return self.name

    def get_url_name(self):
        return self.url_name
