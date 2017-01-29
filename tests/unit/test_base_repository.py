import pytest
from charitybot2.persistence.base_repository import BaseRepository, InvalidRepositoryException
from tests.paths_for_tests import test_repository_db_path, valid_event_config_path


class TestBaseRepositoryInstantiation:
    def test_default_debug_is_false(self):
        base_repository = BaseRepository(db_path=test_repository_db_path)
        assert base_repository.debug is False


class TestBaseRepositoryExceptions:
    @pytest.mark.parametrize('db_path', [
        '',
        'Bla',
        None,
        123
    ])
    def test_passing_incorrect_db_paths_throws_exception(self, db_path):
        with pytest.raises(FileNotFoundError):
            BaseRepository(db_path=db_path)

    def test_passing_non_db_path_throws_exception(self):
        non_db_path = valid_event_config_path
        with pytest.raises(InvalidRepositoryException):
            BaseRepository(db_path=non_db_path)
