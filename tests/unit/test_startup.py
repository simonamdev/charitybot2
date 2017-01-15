import pytest
from charitybot2.charitybot2 import BotStartupValidator, MissingRequiredFolderException, MissingRequiredFileException
from tests.test_helpers import TestFilePath


class TestDirectoryValidation:
    def test_checking_folder_that_does_not_exist_throws_exception(self):
        with pytest.raises(MissingRequiredFolderException):
            validator = BotStartupValidator(db_directory='bla', config_directory='foo')
        with pytest.raises(MissingRequiredFolderException):
            validator = BotStartupValidator(db_directory=TestFilePath().db_dir, config_directory='car')
        with pytest.raises(MissingRequiredFolderException):
            validator = BotStartupValidator(db_directory='coo', config_directory=TestFilePath().config_dir)


class TestFileValidation:
    validator = BotStartupValidator(db_directory=TestFilePath().db_dir, config_directory=TestFilePath().config_dir)

    def test_given_existing_config_name_exists(self):
        self.validator.confirm_config_exists(config_type='base', file_name='valid_config.json')

    def test_given_non_existing_file_name_throws_exception(self):
        with pytest.raises(MissingRequiredFileException):
            self.validator.confirm_config_exists(config_type='meow', file_name='hiss')
