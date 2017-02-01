import pytest
from charitybot2.models.event import Event
from charitybot2.paths import production_repository_db_path
from charitybot2.persistence.event_repository import EventRepository
from tests.paths_for_tests import test_repository_db_path


test_event_repository = EventRepository(debug=True)


class TestEventRepositoryInstantiation:
    def test_default_debug_is_false(self):
        event_repository = EventRepository()
        assert event_repository.debug is False

    @pytest.mark.parametrize('debug,path', [
        (True, test_repository_db_path),
        (False, production_repository_db_path)
    ])
    def test_repository_paths(self, debug, path):
        event_repository = EventRepository(debug=debug)
        assert event_repository.db_path == path


class TestEventRepository:
    def test_get_event(self):
        event = test_event_repository.get_event(identifier='test_event_1')
        assert isinstance(event, Event)
