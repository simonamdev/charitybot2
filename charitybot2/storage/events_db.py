import uuid

from charitybot2.storage.base_db import BaseDB

events_db_file_name = 'events.db'


class EventAlreadyRegisteredException(Exception):
    pass


class EventGivenInvalidStateException(Exception):
    pass


class EventsDB(BaseDB):
    event_registered_state = 'REGISTERED'
    event_ongoing_state = 'ONGOING'
    event_completed_state = 'COMPLETED'
    event_default_state = event_registered_state
    event_possible_states = [
        'REGISTERED',
        'ONGOING',
        'COMPLETED'
    ]

    def __init__(self, db_path=events_db_file_name, verbose=False):
        super().__init__(file_path=db_path, db_name='Events DB', verbose=verbose)

    def print(self, print_string):
        if self.verbose:
            print('[EDB] ' + print_string)

    def event_exists(self, event_name):
        return event_name in self.get_all_event_names()

    def get_all_event_names(self):
        return [row[1] for row in self.db.get_all_rows(table='events')]

    def get_event_metadata(self, event_name):
        row = self.db.get_specific_rows(table='events', filter_string='name = \'{}\''.format(event_name))[0]
        return {
            'name': row[1],
            'uuid': row[2],
            'state': row[3]
        }

    def get_event_state(self, event_name):
        return self.get_event_metadata(event_name=event_name)['state']

    def register_event(self, event_name):
        if event_name in self.get_all_event_names():
            raise EventAlreadyRegisteredException('Event with name: {} is already registered'.format(event_name))
        event_uuid = uuid.uuid4().bytes
        self.db.insert_row(table='events', row_string='(NULL, ?, ?, ?)', row_data=(event_name, event_uuid, EventsDB.event_default_state))

    def change_event_state(self, event_name, new_state):
        if new_state not in EventsDB.event_possible_states:
            raise EventGivenInvalidStateException
        self.db.update_rows(table='events', update_string='state = ?', update_values=(new_state,), filter_string='name = \'{}\''.format(event_name))
