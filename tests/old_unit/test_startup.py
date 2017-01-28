import pytest
from charitybot2.charitybot2 import BotStartupValidator, MissingRequiredFolderException, MissingRequiredFileException
from tests.paths_for_tests import TestFilePath


class TestDirectoryValidation:
    @pytest.mark.parametrize('db_dir,config_dir', [
        ('foo',                'bar'),
        (TestFilePath().db_dir, 'cat'),
        ('dog',                 TestFilePath().config_dir),
        ('',                    'cow'),
        ('horse',               ''),
        ('',                    '')
    ])
    def test_checking_folder_that_does_not_exist_throws_exception(self, db_dir, config_dir):
        with pytest.raises(MissingRequiredFolderException):
            validator = BotStartupValidator(db_directory=db_dir, config_directory=config_dir)


class TestFileValidation:
    validator = BotStartupValidator(db_directory=TestFilePath().db_dir, config_directory=TestFilePath().config_dir)

    def test_given_existing_config_name_exists(self):
        self.validator.confirm_config_exists(config_type='base', file_name='valid_config.json')

    @pytest.mark.parametrize('config_type,file_name', [
        ('',    ''),
        ('foo', ''),
        ('',    'bar'),
        ('foo', 'bar')
    ])
    def test_given_non_existing_file_name_throws_exception(self, config_type, file_name):
        with pytest.raises(MissingRequiredFileException):
            self.validator.confirm_config_exists(config_type=config_type, file_name=file_name)
