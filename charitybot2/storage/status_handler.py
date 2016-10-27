class StatusHandler:
    def __init__(self, db_handler):
        self.db_handler = db_handler
        self.events_db = self.db_handler.get_events_db()
        self.donations_db = self.db_handler.get_events_db()

    def get_events(self, state):
        return [row for row in self.events_db.get_data_for_all_events() if row.get_state() == state]
