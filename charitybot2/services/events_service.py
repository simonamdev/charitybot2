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
        return self._event_repository.get_all_identifiers()

    """
    Check if an event is registered
    """
    def event_is_registered(self, event_identifier):
        return self._event_repository.event_already_registered(identifier=event_identifier)

    """
    If an event exists, retrieve its configuration
    """
    def get_event_configuration(self, event_identifier):
        return self._event_repository.get_event_configuration(identifier=event_identifier)

    """
    Register a new event
    """
    def register_event(self, event_configuration):
        self._event_repository.register_event(event_configuration=event_configuration)

    """
    Update an existing event
    """
    def update_event(self, event_configuration):
        self._event_repository.update_event(new_event_configuration=event_configuration)

    """
    Get the total raised for a given event
    """
    def get_event_total(self, event_identifier):
        return self._event_repository.get_event_current_amount(identifier=event_identifier)

    """
    Set the total raised for a given event
    """
    def set_event_total(self, event_identifier, total):
        self._event_repository.update_event_current_amount(identifier=event_identifier, current_amount=total)

    """
    Set the event target amount
    """
    def set_event_target(self, event_identifier, target):
        self._event_repository.update_event_target_amount(identifier=event_identifier, target_amount=target)

    """
    Retrieve the events that are currently ongoing
    Optional parameter <current_time> allows us to get ongoing events at arbitrary times. Leaving it none will use the current time
    Optional parameter <buffer_in_minutes> is the amount of leeway to add in minutes at the start and end of a stream
    """
    def get_ongoing_events(self, current_time=None, buffer_in_minutes=15):
        return self._event_repository.get_ongoing_events(current_time=current_time, buffer_in_minutes=buffer_in_minutes)

    """
    Retrieve the upcoming events.
    Optional parameter <current_time> allows us to get upcoming events after an arbitrary time.
    Optional parameter <hours in advance> allows us to set
    """
    def get_upcoming_events(self, current_time=None, hours_in_advance=24):
        return self._event_repository.get_upcoming_events(current_time=current_time, hours_in_advance=hours_in_advance)
