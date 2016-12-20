from charitybot2.charitybot2 import create_cb_process_parser, CharityBot

args = create_cb_process_parser().parse_args()
bot = CharityBot(args=args)
bot.initialise_bot()
bot.start_bot()
