from charitybot2.persistence.event_sqlite_repository import EventSQLiteRepository


class EventsService:
    def __init__(self, repository_path):
        self._repository_path = repository_path
        self._event_repository = None

    """
    Opens the connections to the repositories required
    """
    def open_connections(self):
        if self._event_repository is None:
            self._event_repository = EventSQLiteRepository(db_path=self._repository_path)

    """
    Closes the connections to the repositories
    """
    def close_connections(self):
        self._event_repository.close_connection()
