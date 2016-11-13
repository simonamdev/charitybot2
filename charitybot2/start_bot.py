import argparse

from charitybot2.charitybot2 import BotStartupValidator
from tests.tests import TestFilePath


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
        self.debug = True if self.args.debug is not None else False
        self.twitch_mode = True if self.args.twitch_config else False
        self.validate_bot()

    def validate_bot(self):
        if self.args.event == '':
            raise IllegalArgumentException('Empty event config file name passed')
        validator = BotStartupValidator(db_directory=TestFilePath().db_dir, config_directory=TestFilePath().config_dir) if self.debug else BotStartupValidator()
        validator.confirm_config_exists('event', self.args.event + '.json')
        if self.twitch_mode:
            validator.confirm_config_exists('twitch', self.args.twitch_config + '.json')

    def start_bot(self):
        pass


if __name__ == '__main__':
    args = create_parser().parse_args()
    CharityBot(args=args)
