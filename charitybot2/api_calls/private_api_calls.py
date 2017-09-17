import json

import time

from charitybot2.configurations.event_configuration import EventConfiguration
from charitybot2.exceptions import IllegalArgumentException
from charitybot2.models.donation import Donation
from charitybot2.models.event import NonExistentEventException
from charitybot2.sources.url_call import UrlCall
from type_assertions import accept_types


class PrivateApiCalls:
    def __init__(self, base_api_url, timeout=2):
        self._timeout = timeout
        self._base_api_url = base_api_url + 'api/v1/'

    def __validate_event_identifier(self, event_identifier):
        if ' ' in event_identifier:
            raise NonExistentEventException('Event identifiers cannot contain spaces')
        if not self.get_event_existence(identifier=event_identifier):
            raise NonExistentEventException('Event with identifier {} does not exist'.format(event_identifier))

    def get_index(self):
        return json.loads(UrlCall(url=self._base_api_url, timeout=self._timeout).get().content.decode('utf-8'))

    @accept_types(object, str)
    def get_event_existence(self, identifier):
        url = self._base_api_url + 'event/exists/{}/'.format(identifier)
        decoded_content = UrlCall(url=url, timeout=self._timeout).get().content.decode('utf-8')
        return json.loads(decoded_content)['event_exists']

    @accept_types(object, str)
    def get_event_info(self, identifier):
        url = self._base_api_url + 'event/{}'.format(identifier)
        decoded_content = UrlCall(url=url, timeout=self._timeout).get().content.decode('utf-8')
        content = json.loads(decoded_content)
        if 'message' in content.keys():
            raise NonExistentEventException('Event with identifier {} does not exist'.format(identifier))
        return content

    @accept_types(object, EventConfiguration)
    def register_event(self, event_configuration):
        url = self._base_api_url + 'event/'
        response = UrlCall(url=url, timeout=self._timeout).post(data=event_configuration.configuration_values)
        decoded_content = response.content.decode('utf-8')
        return json.loads(decoded_content)['registration_successful']

    @accept_types(object, EventConfiguration)
    def update_event(self, event_configuration):
        url = self._base_api_url + 'event/'
        response = UrlCall(url=url, timeout=self._timeout).post(data=event_configuration.configuration_values)
        decoded_content = response.content.decode('utf-8')
        return json.loads(decoded_content)['update_successful']

    @accept_types(object, str, str, (int, float))
    def send_heartbeat(self, source, state, timestamp=None):
        if timestamp is None or not isinstance(timestamp, int):
            timestamp = int(time.time())
        data = dict(state=state, source=source, timestamp=timestamp)
        url = self._base_api_url + 'heartbeat/'
        response = UrlCall(url=url, timeout=self._timeout).post(data=data)
        decoded_content = response.content.decode('utf-8')
        return json.loads(decoded_content)['received']

    # Disabled due to assertion check not working properly for this specific method
    # @accept_types(object, Donation)
    def register_donation(self, donation):
        url = self._base_api_url + 'donation/'
        response = UrlCall(url=url, timeout=self._timeout).post(data=donation.to_dict())
        decoded_content = response.content.decode('utf-8')
        return json.loads(decoded_content)['received']

    def get_event_donations(self, event_identifier, time_bounds=(), limit=None):
        self.__validate_event_identifier(event_identifier=event_identifier)
        params_added = False
        # TODO: Rewrite to properly use query parameters built into requests instead of manually concatenating
        url = self._base_api_url + 'event/{}/donations/'.format(event_identifier)
        if len(time_bounds) == 2:
            lower_bound, upper_bound = time_bounds[0], time_bounds[1]
            if not isinstance(lower_bound, int) or not isinstance(upper_bound, int):
                raise IllegalArgumentException('Time bounds must be a tuple of 2 integers')
            url += '?lower={}&upper={}'.format(lower_bound, upper_bound)
            params_added = True
        if limit is not None:
            if limit <= 0:
                raise IllegalArgumentException('Limit must be 1 or more')
            url += '&' if params_added else '?'
            url += 'limit={}'.format(limit)
            params_added = True
        response = UrlCall(url=url, timeout=self._timeout).get()
        decoded_content = response.content.decode('utf-8')
        converted_content = json.loads(decoded_content)['donations']
        if isinstance(converted_content, list):
            donations = [Donation.from_json(donation) for donation in converted_content]
        else:
            donations = Donation.from_json(converted_content)
        return donations

    def get_last_event_donation(self, event_identifier):
        return self.get_event_donations(event_identifier=event_identifier, limit=1)

    def get_event_total(self, event_identifier):
        self.__validate_event_identifier(event_identifier=event_identifier)
        url = self._base_api_url + 'event/{}/total/'.format(event_identifier)
        response = UrlCall(url=url, timeout=self._timeout).get()
        decoded_content = response.content.decode('utf-8')
        return float(json.loads(decoded_content)['total'])

    def get_latest_event_donation(self, event_identifier):
        self.__validate_event_identifier(event_identifier=event_identifier)
        url = self._base_api_url + 'event/{}/donations/largest'.format(event_identifier)
        response = UrlCall(url=url, timeout=self._timeout).get()
        decoded_content = response.content.decode('utf-8')
        converted_content = json.loads(decoded_content)
        return Donation.from_dict(converted_content)

    def get_donation_count(self, event_identifier):
        self.__validate_event_identifier(event_identifier=event_identifier)
        url = self._base_api_url + 'event/{}/donations/count'.format(event_identifier)
        response = UrlCall(url=url, timeout=self._timeout).get()
        decoded_content = response.content.decode('utf-8')
        converted_content = json.loads(decoded_content)
        return int(converted_content['count'])

    def get_time_bound_donation_count(self, event_identifier, lower_time_bound, upper_time_bound):
        self.__validate_event_identifier(event_identifier=event_identifier)
        if not isinstance(lower_time_bound, int) or not isinstance(upper_time_bound, int):
            raise IllegalArgumentException('Time bounds must be integers')
        if not upper_time_bound > lower_time_bound or (lower_time_bound < 0 or upper_time_bound < 0):
            raise IllegalArgumentException('Time bounds must be positive integers with upper larger than lower')
        url = self._base_api_url + 'event/{}/donations/count?lower={}&upper={}'.format(
            event_identifier,
            lower_time_bound,
            upper_time_bound)
        response = UrlCall(url=url, timeout=self._timeout).get()
        decoded_content = response.content.decode('utf-8')
        converted_content = json.loads(decoded_content)
        return int(converted_content['count'])

    def get_average_donation_amount(self, event_identifier):
        self.__validate_event_identifier(event_identifier=event_identifier)
        url = self._base_api_url + 'event/{}/donations/average'.format(
            event_identifier
        )
        response = UrlCall(url=url, timeout=self._timeout).get()
        decoded_content = response.content.decode('utf-8')
        converted_content = json.loads(decoded_content)
        return round(float(converted_content['average_donation_amount']), 3)

    def get_donation_distribution(self, event_identifier):
        self.__validate_event_identifier(event_identifier=event_identifier)
        url = self._base_api_url + 'event/{}/donations/distribution'.format(
            event_identifier
        )
        response = UrlCall(url=url, timeout=self._timeout).get()
        decoded_content = response.content.decode('utf-8')
        converted_content = json.loads(decoded_content)
        return converted_content['distribution']
