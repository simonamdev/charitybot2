import json

from charitybot2.private_api.private_api import private_api_full_url
from charitybot2.sources.url_call import UrlCall


class PrivateApiCalls:
    v1_url = private_api_full_url + 'api/v1/'

    def __init__(self, timeout=2):
        self._timeout = timeout

    def get_index(self):
        return json.loads(UrlCall(url=self.v1_url, timeout=self._timeout).get().content.decode('utf-8'))

    def get_event_existence(self, identifier):
        url = self.v1_url + 'event/exists/{}/'.format(identifier)
        decoded_content = UrlCall(url=url, timeout=self._timeout).get().content.decode('utf-8')
        return json.loads(decoded_content)['event_exists']

    def get_event_info(self, identifier):
        url = self.v1_url + 'event/{}'.format(identifier)
        decoded_content = UrlCall(url=url, timeout=self._timeout).get().content.decode('utf-8')
        content = json.loads(decoded_content)
        return content if len(content.keys()) > 0 else None

    def register_event(self, event_configuration):
        url = self.v1_url + 'event/register/'
        response = UrlCall(url=url, timeout=self._timeout).post(data=event_configuration.configuration_values)
        decoded_content = response.content.decode('utf-8')
        return json.loads(decoded_content)['registration_successful']

    def update_event(self, event_configuration):
        url = self.v1_url + 'event/update/'
        response = UrlCall(url=url, timeout=self._timeout).post(data=event_configuration.configuration_values)
        decoded_content = response.content.decode('utf-8')
        return json.loads(decoded_content)['update_successful']
