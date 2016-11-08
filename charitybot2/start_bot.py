import argparse


def setup_argument_parser():
    parser = argparse.ArgumentParser(description='Charity stream bot')
    parser.add_argument('--event-config', type=str, help='Event Config file name')
    parser.add_argument('--twitch-config', type=str, help='Twitch Bot Config file name')
    return parser


def start_bot():
    args = setup_argument_parser().parse_args()
    print(args)
    print(args.event_config)

if __name__ == '__main__':
    start_bot()
