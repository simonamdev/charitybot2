import uuid

from charitybot2.storage.base_db import BaseDB
from charitybot2.storage.logger import Logger

events_db_file_name = 'events.db'


class EventAlreadyRegisteredException(Exception):
    pass


class EventGivenInvalidStateException(Exception):
    pass


class EventMetadata:
    registered_state = 'REGISTERED'
    ongoing_state = 'ONGOING'
    completed_state = 'COMPLETED'
    default_state = registered_state
    event_possible_states = [registered_state, ongoing_state, completed_state]

    def __init__(self, name, state):
        self.name = name
        self.state = state

    def get_name(self):
        return self.name

    def get_state(self):
        return self.state


class EventsDB(BaseDB):
    def __init__(self, db_path=events_db_file_name, debug=False):
        super().__init__(file_path=db_path, db_name='Events DB', verbose=debug)
        self.logger = Logger(source='EventsDB', console_only=debug)

    def event_exists(self, event_name):
        return event_name in self.get_all_event_names()

    def get_all_event_names(self):
        self.logger.log_info('Retrieving all event names')
        return [row[1] for row in self.db.get_all_rows(table='events')]

    def get_data_for_all_events(self):
        self.logger.log_info('Retrieving data for all events')
        return [self.convert_to_event_metadata(row) for row in self.db.get_all_rows(table='events')]

    def convert_to_event_metadata(self, event_db_row):
        return EventMetadata(name=event_db_row[1], state=event_db_row[2])

    def get_event_metadata(self, event_name):
        row = self.db.get_specific_rows(table='events', filter_string='name = \'{}\''.format(event_name))[0]
        return self.convert_to_event_metadata(row)

    def get_event_state(self, event_name):
        return self.get_event_metadata(event_name=event_name).get_state()

    def register_event(self, event_name):
        if event_name in self.get_all_event_names():
            raise EventAlreadyRegisteredException('Event with name: {} is already registered'.format(event_name))
        self.db.insert_row(table='events', row_string='(NULL, ?, ?)', row_data=(event_name, EventMetadata.registered_state))

    def change_event_state(self, event_name, new_state):
        if new_state not in EventMetadata.event_possible_states:
            raise EventGivenInvalidStateException
        self.db.update_rows(table='events', update_string='state = ?', update_values=(new_state,), filter_string='name = \'{}\''.format(event_name))
