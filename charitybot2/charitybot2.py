import os
import argparse

from charitybot2.config.twitch_config import TwitchAccountConfiguration
from charitybot2.events.event import Event
from charitybot2.events.event_loop import TwitchEventLoop, EventLoop
from charitybot2.reporter.twitch import TwitchAccount
from charitybot2.storage.db_handler import DBHandler
from tests.tests import TestFilePath
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
        if not os.path.isfile(os.path.join(self.config_directory, config_type, file_name)):
            raise MissingRequiredFileException


class IllegalArgumentException(Exception):
    pass


def create_parser():
    parser = argparse.ArgumentParser(description='Charity stream bot')
    parser.add_argument('event', type=str, help='Event Configuration file name')
    parser.add_argument('--twitch-config', type=str, help='Twitch Bot Config file name')
    parser.add_argument('--debug', dest='debug', help='Run CharityBot in debug mode', action='store_true')
    return parser


class CharityBot:
    def __init__(self, args):
        self.args = args
        self.event_config_path = None
        self.debug = True if self.args.debug is not None else False
        self.db_dir = TestFilePath().db_dir if self.debug else paths.db_folder
        self.donations_db_path = os.path.join(self.db_dir, 'donations.db')
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
        db_handler = DBHandler(donations_db_path=self.donations_db_path, debug=self.debug)
        event = Event(config_path=self.event_config_path, db_handler=db_handler)
        twitch_config_path = os.path.join(self.config_dir, 'twitch', self.args.twitch_config + '.json') if self.twitch_mode else None
        twitch_config = TwitchAccountConfiguration(file_path=twitch_config_path) if self.twitch_mode else None
        twitch_account = TwitchAccount(twitch_config=twitch_config) if self.twitch_mode else None
        self.event_loop = TwitchEventLoop(event=event, twitch_account=twitch_account, debug=self.debug) if self.twitch_mode else EventLoop(event=event, debug=self.debug)

    def start_bot(self):
        self.event_loop.start()


if __name__ == '__main__':
    args = create_parser().parse_args()
    CharityBot(args=args)
