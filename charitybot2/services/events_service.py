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

    """
    Get all registered event names
    """
    def get_all_event_identifiers(self):
        pass

    """
    Check if an event is registered
    """
    def event_is_registered(self, event_identifier):
        pass

    """
    If an event exists, retrieve its configuration
    """
    def get_event_configuration(self, event_identifier):
        pass

    """
    Register a new event
    """
    def register_event(self, event_identifier):
        pass

    """
    Update an existing event
    """
    def update_event(self, event_identifier):
        pass

    """
    Set the total raised for a given event
    """
    def set_event_total(self, event_identifier, total):
        pass

