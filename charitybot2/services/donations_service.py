from charitybot2.persistence.donation_sqlite_repository import DonationSQLiteRepository
from charitybot2.persistence.event_sqlite_repository import EventSQLiteRepository


class DonationsService:
    def __init__(self, repository_path):
        self._repository_path = repository_path
        self._event_repository = None
        self._donations_repository = None

    """
    Opens the connections to the repositories required
    """
    def open_connections(self):
        if self._event_repository is None:
            self._event_repository = EventSQLiteRepository(db_path=self._repository_path)
        if self._donations_repository is None:
            self._donations_repository = DonationSQLiteRepository(db_path=self._repository_path)

    """
    Closes the connections to the repositories
    """
    def close_connections(self):
        self._event_repository.close_connection()
        self._donations_repository.close_connection()

    """
    Retrieve all donations for a given event
    """
    def get_all_donations(self, event_identifier):
        return self._donations_repository.get_event_donations(event_identifier=event_identifier)

    """
    Retrieve the latest donation for a given event
    """
    def get_latest_donation(self, event_identifier):
        return self._donations_repository.get_latest_event_donation(event_identifier=event_identifier)

    """
    Retrieve the latest few donations for a given event, in descending order by the datetime of donation
    """
    def get_latest_donations(self, event_identifier, limit):
        return None

    """
    Retrieve the largest donation for a given event.
    Largest donation is the donation with the highest amount donated
    """
    def get_largest_donation(self, event_identifier):
        return self._donations_repository.get_largest_donation(event_identifier=event_identifier)
