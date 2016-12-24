from charitybot2.charitybot2 import create_cb_process_parser, CharityBot
from charitybot2.events.event import EventAlreadyFinishedException

args = create_cb_process_parser().parse_args()
bot = CharityBot(args=args)
try:
    bot.initialise_bot()
except EventAlreadyFinishedException:
    print('Event end time is in the past - check your configuration file')
    quit(1)
bot.start_bot()
