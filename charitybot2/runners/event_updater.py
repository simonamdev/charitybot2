from charitybot2.api.donations_api import full_url as donations_api_url
from charitybot2.api.events_api import full_url as events_api_url
from charitybot2.api_calls.donations_api_wrapper import DonationsApiWrapper
from charitybot2.api_calls.events_api_wrapper import EventsApiWrapper

donations_api_wrapper = DonationsApiWrapper(base_url=donations_api_url)
events_api_wrapper = EventsApiWrapper(base_url=events_api_url)


class EventUpdater:
    pass
