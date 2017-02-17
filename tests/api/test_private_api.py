from charitybot2.api_calls.private_api_calls import PrivateApiCalls
from charitybot2.creators.event_creator import EventRegister
from charitybot2.persistence.event_sqlite_repository import EventSQLiteRepository
from charitybot2.private_api.private_api import private_api_identity
from tests.integration.test_event_register import get_test_configuration
from tests.mocks import MockPrivateAPI, WipeSQLiteDB
from tests.paths_for_tests import test_repository_db_path

mock_private_api = MockPrivateAPI()
private_api_calls = PrivateApiCalls()


def setup_test_database():
    print('Setting up test database ')
    WipeSQLiteDB(db_path=test_repository_db_path).wipe_db()
    updated_values = {
        'identifier': 'test',
        'title': 'Test Event'
    }
    event_repository = EventSQLiteRepository(db_path=test_repository_db_path)
    event_register = EventRegister(
        event_configuration=get_test_configuration(updated_values=updated_values),
        event_repository=event_repository)
    event_register.get_event()


def setup_module():
    setup_test_database()
    mock_private_api.start()


def teardown_module():
    mock_private_api.stop()


class TestStartup:
    def test_getting_identity_string(self):
        response = private_api_calls.get_index()
        assert isinstance(response['identity'], str)
        assert private_api_identity == response['identity']
        assert isinstance(response['version'], int)
        assert 1 == response['version']
        assert True is response['debug']


class TestEventInformation:
    def test_getting_event_info_of_non_existent_returns_false_existence(self):
        response = private_api_calls.get_event_existence('foobar')
        assert False is response

    def test_getting_event_info_for_existence(self):
        response = private_api_calls.get_event_existence(identifier='test')
        assert True is response


class TestEventRegistration:
    def test_registering_new_event(self):
        updated_values = {
            'identifier': 'registration_test',
            'title': 'Registration Test Event'
        }
        registration_test_configuration = get_test_configuration(updated_values=updated_values)
        response = private_api_calls.register_event(event_configuration=registration_test_configuration)
        assert True is response

    def test_updating_new_event(self):
        updated_values = {
            'identifier': 'update_test',
            'title': 'Update Test Event'
        }
        registration_test_configuration = get_test_configuration(updated_values=updated_values)
        response = private_api_calls.register_event(event_configuration=registration_test_configuration)
        assert True is response
        updated_values = {
            'identifier': 'update_test',
            'start_time': 500,
            'end_time': 1000
        }
        update_test_configuration = get_test_configuration(updated_values=updated_values)
        response = private_api_calls.update_event(event_configuration=update_test_configuration)
        assert True is response
