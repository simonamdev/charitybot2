from charitybot2.storage.events_db import EventMetadata


class StatusHandler:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def get_running_events(self):
        return [row for row in self.db_handler.get_events_db().get_data_for_all_events() if row.get_state() == EventMetadata.ongoing_state]
