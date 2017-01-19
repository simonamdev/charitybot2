import os
import argparse

from charitybot2.botconfig.event_config import EventConfigurationFromFile
from charitybot2.botconfig.twitch_config import TwitchAccountConfiguration
from charitybot2.events.event import Event
from charitybot2.events.event_loop import TwitchEventLoop, EventLoop
from charitybot2.reporter.twitch import TwitchAccount
from tests.paths_for_tests import TestFilePath
from charitybot2 import paths


class MissingRequiredFolderException(Exception):
    pass


class MissingRequiredFileException(Exception):
    pass


class BotStartupValidator:
    def __init__(self, db_directory, config_directory):
        self.db_directory = db_directory
        self.config_directory = config_directory
        self.confirm_directories_exist()

    def confirm_directories_exist(self):
        if not os.path.isdir(self.config_directory) or not os.path.isdir(self.db_directory):
            raise MissingRequiredFolderException('Either config or DB directories are missing')

    def confirm_config_exists(self, config_type, file_name):
        config_path = os.path.join(self.config_directory, config_type, file_name)
        if not os.path.isfile(config_path):
            raise MissingRequiredFileException('Configuration file does not exist: {}'.format(config_path))


class IllegalArgumentException(Exception):
    pass


def create_cb_process_parser():
    parser = argparse.ArgumentParser(description='Charitybot Process')
    parser.add_argument('event', type=str, help='Event Configuration file name')
    parser.add_argument('--twitch-config', type=str, help='Twitch Bot Config file name')
    parser.add_argument('--debug', dest='debug', help='Run Charitybot in debug mode', action='store_true')
    return parser


class CharityBot:
    def __init__(self, args):
        self.args = args
        self.event_config_path = None
        self.debug = self.args.debug
        self.db_dir = TestFilePath().db_dir if self.debug else paths.db_folder
        self.db_path = os.path.join(self.db_dir, 'repository.db')
        self.config_dir = TestFilePath().config_dir if self.debug else paths.config_folder
        self.twitch_mode = True if self.args.twitch_config else False
        self.validate_bot()
        self.event_loop = None

    def validate_bot(self):
        if self.args.event == '':
            raise IllegalArgumentException('Empty event config file name passed')
        validator = BotStartupValidator(db_directory=self.db_dir, config_directory=self.config_dir)
        event_config_filename = self.args.event + '.json'
        validator.confirm_config_exists('event', event_config_filename)
        self.event_config_path = os.path.join(self.config_dir, 'event', event_config_filename)
        if self.twitch_mode:
            validator.confirm_config_exists('twitch', self.args.twitch_config + '.json')

    def initialise_bot(self):
        event_config = EventConfigurationFromFile(file_path=self.event_config_path).get_event_configuration()
        event = Event(event_configuration=event_config, db_path=self.db_path)
        if self.twitch_mode:
            twitch_config_path = os.path.join(self.config_dir, 'twitch', self.args.twitch_config + '.json')
            twitch_config = TwitchAccountConfiguration(file_path=twitch_config_path)
            twitch_account = TwitchAccount(twitch_config=twitch_config)
            self.event_loop = TwitchEventLoop(event=event, twitch_account=twitch_account, debug=self.debug)
        else:
            self.event_loop = EventLoop(event=event, debug=self.debug)

    def start_bot(self):
        self.event_loop.start()



