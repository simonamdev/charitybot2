class StatusHandler:
    def __init__(self, db_handler):
        self.db_handler = db_handler
        self.donations_db = self.db_handler.get_donations_db()

    def get_donations(self, event):
        return
