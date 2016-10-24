import os
import pytest

from time import sleep
from charitybot2.storage.logs_db import LogsDB, LogSourceDoesNotExistException, Log

current_directory = os.path.dirname(os.path.abspath(__file__))
test_db_path = os.path.join(current_directory, 'db', 'logs.db')


def setup_module():
    if os.path.isfile(test_db_path):
        os.remove(test_db_path)
    sleep(0.5)
    open(test_db_path, 'w')


class TestLogsDatabaseTableCRUD:
    def test_db_resetting_for_tests(self):
        db = LogsDB(db_path=test_db_path, verbose=True)
        assert db.get_available_log_sources() == []

    def test_log_source_table_creation(self):
        db = LogsDB(db_path=test_db_path, verbose=True)
        db.create_log_source_table(log_source='test_one')
        assert 'test_one' in db.get_available_log_sources()

    def test_creating_two_tables_with_same_name_processes_normally(self):
        db = LogsDB(db_path=test_db_path, verbose=True)
        db.create_log_source_table(log_source='test_two')
        db.create_log_source_table(log_source='test_two')

    def test_no_logs_returned_from_empty_source(self):
        db = LogsDB(db_path=test_db_path, verbose=True)
        assert [] == db.get_all_logs(source='test_two')

    def test_info_logging_to_existing_log_source(self):
        db = LogsDB(db_path=test_db_path, verbose=True)
        db.create_log_source_table(log_source='test_three')
        db.log(source='test_three', level=Log.info_level, message='Foo')
        print(db.get_all_logs(source='test_three')[0])
        assert 'Foo' == db.get_all_logs(source='test_three')[0].get_message()

    def test_logging_to_warning_returns_warning_level(self):
        db = LogsDB(db_path=test_db_path, verbose=True)
        db.log(source='test_three', level=Log.warning_level, message='Bla')
        assert Log.warning_level == db.get_all_logs(source='test_three')[1].get_level()

    def test_logging_to_non_existent_log_source_throws_exception(self):
        db = LogsDB(db_path=test_db_path, verbose=True)
        with pytest.raises(LogSourceDoesNotExistException):
            db.log(source='test_four', level=Log.info_level, message='Foo')
