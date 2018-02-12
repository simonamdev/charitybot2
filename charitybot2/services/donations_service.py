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
    Retrieve the number of donations for a given event
    """
    def get_number_of_donations(self, event_identifier):
        pass

    """
    Retrieve the latest number of donations for a given event, in descending order by the datetime of donation
    """
    def get_latest_donations(self, event_identifier, limit):
        return self._donations_repository.get_event_donations(event_identifier=event_identifier, limit=limit)

    """
    Retrieve the latest donation for a given event
    """
    def get_latest_donation(self, event_identifier):
        latest_donations = self.get_latest_donations(event_identifier=event_identifier, limit=1)
        return latest_donations[0] if len(latest_donations) == 1 else None

    """
    Retrieve the largest donation for a given event.
    Largest donation is the donation with the highest amount donated
    """
    def get_largest_donation(self, event_identifier):
        return self._donations_repository.get_largest_donation(event_identifier=event_identifier)

    """
    Retrieve the average donation for a given event.
    """
    def get_average_donation(self, event_identifier):
        return self._donations_repository.get_average_donation_amount(event_identifier=event_identifier)

    """
    Retrieve donations for a given event between certain time bounds.
    Return all donations if no limit or time bounds are given.
    """
    def get_time_bounded_donations(self, event_identifier, lower_bound=None, upper_bound=None, limit=None):
        # If no parameters are passed, just return all the donations
        if lower_bound is None and upper_bound is None and limit is None:
            return self.get_all_donations(event_identifier=event_identifier)
        if lower_bound is None and upper_bound is None:
            return self.get_latest_donations(event_identifier=event_identifier, limit=limit)
        if upper_bound is None and limit is None:
            return self._donations_repository.get_time_filtered_event_donations(
                event_identifier=event_identifier,
                lower_bound=lower_bound)
        if lower_bound is None and limit is None:
            return self._donations_repository.get_time_filtered_event_donations(
                event_identifier=event_identifier,
                lower_bound=0,
                upper_bound=upper_bound)
        if limit is None:
            return self._donations_repository.get_time_filtered_event_donations(
                event_identifier=event_identifier,
                lower_bound=lower_bound,
                upper_bound=upper_bound)
        return self._donations_repository.get_time_filtered_event_donations(
                event_identifier=event_identifier,
                lower_bound=lower_bound,
                upper_bound=upper_bound,
                limit=limit)
