import json

from charitybot2.creators.event_configuration_creator import EventConfigurationCreator, \
    InvalidEventConfigurationException
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
        print(event_configuration.configuration_values)
        response = UrlCall(url=url, timeout=self._timeout).send_json(
            data=event_configuration.configuration_values)
        decoded_content = response.content.decode('utf-8')
        converted_content = json.loads(decoded_content)
        successful = converted_content['success']
        if not successful:
            error_message = converted_content['error']
            return error_message
        return successful

    def update_event(self, new_event_configuration):
        url = self._base_url + 'event/{}/update/'.format(new_event_configuration.identifier)
        response = UrlCall(url=url, timeout=self._timeout).send_json(data=new_event_configuration.configuration_values)
        decoded_content = response.content.decode('utf-8')
        converted_content = json.loads(decoded_content)
        successful = converted_content['success']
        if not successful:
            error_message = converted_content['error']
            raise NonExistentEventException(error_message)
        return successful

    def get_event_total_raised(self, event_identifier):
        url = self._base_url + 'event/{}/total/'.format(event_identifier)
        response = UrlCall(url=url, timeout=self._timeout).get()
        decoded_content = response.content.decode('utf-8')
        converted_content = json.loads(decoded_content)
        event_exists = converted_content['exists']
        if not event_exists:
            raise NonExistentEventException('Event with identifier: {} does not exist'.format(event_identifier))
        return converted_content['total']

    def update_event_total(self, event_identifier, new_total):
        url = self._base_url + 'event/{}/total/'.format(event_identifier)
        data = {
            'total': new_total
        }
        response = UrlCall(url=url, timeout=self._timeout).post(data=data)
        decoded_content = response.content.decode('utf-8')
        converted_content = json.loads(decoded_content)
        exists = converted_content['exists']
        if not exists:
            raise NonExistentEventException('Event with identifier: {} does not exist'.format(event_identifier))
        successful = converted_content['success']
        if not successful:
            error_message = converted_content['error']
            raise TypeError(error_message)
        return successful

    def get_ongoing_events(self, current_time=None, buffer_in_minutes=15):
        url = self._base_url + 'events/ongoing/'
        query_params = {
            'current_time': current_time,
            'buffer_time': buffer_in_minutes
        }
        response = UrlCall(url=url, params=query_params, timeout=self._timeout).get()
        decoded_content = response.content.decode('utf-8')
        converted_content = json.loads(decoded_content)
        return converted_content['events']

    def get_upcoming_events(self, current_time=None, hours_in_advance=24):
        url = self._base_url + 'events/upcoming/'
        query_params = {
            'current_time': current_time,
            'hours_in_advance': hours_in_advance
        }
        response = UrlCall(url=url, params=query_params, timeout=self._timeout).get()
        decoded_content = response.content.decode('utf-8')
        converted_content = json.loads(decoded_content)
        return converted_content['events']
