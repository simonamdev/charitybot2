import pytest
from charitybot2.charitybot2 import BotStartupValidator, MissingRequiredFolderException
from tests.tests import TestFilePath


class TestStartupValidation:
    def test_checking_folder_that_does_not_exist_throws_exception(self):
        with pytest.raises(MissingRequiredFolderException):
            validator = BotStartupValidator(db_directory='bla', config_directory='foo')
        with pytest.raises(MissingRequiredFolderException):
            validator = BotStartupValidator(db_directory=TestFilePath().db_dir, config_directory='car')
        with pytest.raises(MissingRequiredFolderException):
            validator = BotStartupValidator(db_directory='coo', config_directory=TestFilePath().config_dir)

    def test_default_directories_do_not_throw_exception(self):
        validator = BotStartupValidator()
