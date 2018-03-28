import json

from charitybot2.creators.event_configuration_creator import EventConfigurationCreator
from charitybot2.models.event import NonExistentEventException
from charitybot2.sources.url_call import UrlCall


class EventsApiWrapper:
    def __init__(self, base_url, version=2, timeout=2, maximum_retry_attempts=3):
        self._base_url = base_url + 'api/v{}/'.format(version)  # TODO: Use path resolving function instead of string concat
        self._timeout = timeout
        self._maximum_retry_attempts = maximum_retry_attempts

    def get_index(self):
        return json.loads(UrlCall(url=self._base_url, timeout=self._timeout).get().content.decode('utf-8'))

    def get_event_exists(self, event_identifier):
        url = self._base_url + 'event/{}/exists/'.format(event_identifier)
        response = UrlCall(url=url, timeout=self._timeout).get()
        decoded_content = response.content.decode('utf-8')
        event_exists = json.loads(decoded_content)['exists']
        return event_exists

    # This may require paging in future
    def get_event_identifiers(self):
        url = self._base_url + 'events/'
        response = UrlCall(url=url, timeout=self._timeout).get()
        decoded_content = response.content.decode('utf-8')
        event_identifiers = json.loads(decoded_content)['identifiers']
        return event_identifiers

    def get_event_info(self, event_identifier):
        url = self._base_url + 'event/{}/'.format(event_identifier)
        response = UrlCall(url=url, timeout=self._timeout).get()
        decoded_content = response.content.decode('utf-8')
        converted_content = json.loads(decoded_content)
        event_exists = converted_content['exists']
        if not event_exists:
            raise NonExistentEventException('Event with identifier: {} does not exist'.format(event_identifier))
        event_info = converted_content['info']
        # Create the configuration from the values
        event_config = EventConfigurationCreator(configuration_values=event_info).configuration
        return event_config

    def register_event(self, event_configuration):
        url = self._base_url + 'event/{}/'.format(event_configuration.identifier)
        response = UrlCall(url=url, timeout=self._timeout).post(data=event_configuration.configuration_values)
        decoded_content = response.content.decode('utf-8')
        converted_content = json.loads(decoded_content)
        successful = converted_content['success']
        if not successful:
            error_message = converted_content['error']
            return error_message
        return successful

    def update_event_configuration(self, new_event_configuration):
        url = self._base_url + 'event/{}/'.format(new_event_configuration.identifier)
        response = UrlCall(url=url, timeout=self._timeout).post(data=new_event_configuration.configuration_values)
        decoded_content = response.content.decode('utf-8')
        converted_content = json.loads(decoded_content)
        successful = converted_content['success']
        if not successful:
            error_message = converted_content['error']
            return error_message
        return successful

    def get_event_total_raised(self, event_identifier):
        return None

    def update_event_total(self, event_identifier, new_total):
        return None


