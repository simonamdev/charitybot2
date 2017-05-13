import json

import time

from charitybot2.configurations.event_configuration import EventConfiguration
from charitybot2.exceptions import IllegalArgumentException
from charitybot2.models.donation import Donation
from charitybot2.models.event import NonExistentEventException
from charitybot2.private_api.private_api import private_api_full_url
from charitybot2.sources.url_call import UrlCall
from type_assertions import accept_types


class PrivateApiCalls:
    v1_url = private_api_full_url + 'api/v1/'

    def __init__(self, timeout=2):
        self._timeout = timeout

    def get_index(self):
        return json.loads(UrlCall(url=self.v1_url, timeout=self._timeout).get().content.decode('utf-8'))

    @accept_types(object, str)
    def get_event_existence(self, identifier):
        url = self.v1_url + 'event/exists/{}/'.format(identifier)
        decoded_content = UrlCall(url=url, timeout=self._timeout).get().content.decode('utf-8')
        return json.loads(decoded_content)['event_exists']

    @accept_types(object, str)
    def get_event_info(self, identifier):
        url = self.v1_url + 'event/{}'.format(identifier)
        decoded_content = UrlCall(url=url, timeout=self._timeout).get().content.decode('utf-8')
        content = json.loads(decoded_content)
        if len(content.keys()) == 0:
            raise NonExistentEventException('Event with identifier {} does not exist'.format(identifier))
        return content

    @accept_types(object, EventConfiguration)
    def register_event(self, event_configuration):
        url = self.v1_url + 'event/'
        response = UrlCall(url=url, timeout=self._timeout).post(data=event_configuration.configuration_values)
        decoded_content = response.content.decode('utf-8')
        return json.loads(decoded_content)['registration_successful']

    @accept_types(object, EventConfiguration)
    def update_event(self, event_configuration):
        url = self.v1_url + 'event/'
        response = UrlCall(url=url, timeout=self._timeout).post(data=event_configuration.configuration_values)
        decoded_content = response.content.decode('utf-8')
        return json.loads(decoded_content)['update_successful']

    @accept_types(object, str, str, (int, float))
    def send_heartbeat(self, source, state, timestamp=None):
        if timestamp is None or not isinstance(timestamp, int):
            timestamp = int(time.time())
        data = dict(state=state, source=source, timestamp=timestamp)
        url = self.v1_url + 'heartbeat/'
        response = UrlCall(url=url, timeout=self._timeout).post(data=data)
        decoded_content = response.content.decode('utf-8')
        return json.loads(decoded_content)['received']

    # Disabled due to assertion check not working properly for this specific method
    # @accept_types(object, Donation)
    def register_donation(self, donation):
        url = self.v1_url + 'donation/'
        response = UrlCall(url=url, timeout=self._timeout).post(data=donation.to_dict())
        decoded_content = response.content.decode('utf-8')
        return json.loads(decoded_content)['received']

    def get_event_donations(self, event_identifier, time_bounds=()):
        if ' ' in event_identifier:
            raise NonExistentEventException('Event identifiers cannot contain spaces')
        if not self.get_event_existence(identifier=event_identifier):
            raise NonExistentEventException('Event with identifier {} does not exist'.format(event_identifier))
        url = self.v1_url + 'event/{}/donations/'.format(event_identifier)
        if len(time_bounds) == 2:
            lower_bound, upper_bound = time_bounds[0], time_bounds[1]
            if not isinstance(lower_bound, int) or not isinstance(upper_bound, int):
                raise IllegalArgumentException('Time bounds must be a tuple of 2 integers')
            url += '?lower={}&upper={}'.format(lower_bound, upper_bound)
        response = UrlCall(url=url, timeout=self._timeout).get()
        decoded_content = response.content.decode('utf-8')
        converted_content = json.loads(decoded_content)['donations']
        donations = [Donation.from_json(donation) for donation in converted_content]
        return donations
